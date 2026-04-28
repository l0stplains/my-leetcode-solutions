"""Shared LeetCode API client.

Self-contained: uses LeetCode's REST endpoint for submissions and the public
GraphQL endpoint for problem metadata. No dependency on the leetcode-export
package, so this folder is portable.

Cookie loading order:
  1. Explicit string passed to load_cookies()
  2. LEETCODE_COOKIES environment variable
  3. .leetcode_cookies file in repo root
  4. Interactive prompt (stdin)
"""

import datetime
import json
import logging
import os
import sys
from time import sleep
from typing import Dict, Iterator, List, Optional

import requests


BASE_URL = "https://leetcode.com"
GRAPHQL_URL = "https://leetcode.com/graphql"
SUBMISSIONS_API_URL = "https://leetcode.com/api/submissions/?offset={}&limit={}"
PROBLEM_URL = "https://leetcode.com/problems/{}/"

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ),
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Referer": "https://leetcode.com/",
}

LANG_TO_EXTENSION = {
    "python": "py",
    "python3": "py",
    "pythondata": "py",
    "pythonml": "py",
    "c": "c",
    "cpp": "cpp",
    "csharp": "cs",
    "java": "java",
    "kotlin": "kt",
    "mysql": "sql",
    "mssql": "sql",
    "oraclesql": "sql",
    "javascript": "js",
    "typescript": "ts",
    "html": "html",
    "php": "php",
    "golang": "go",
    "scala": "scala",
    "rust": "rs",
    "ruby": "rb",
    "bash": "sh",
    "swift": "swift",
    "elixir": "ex",
    "erlang": "erl",
    "racket": "rkt",
    "dart": "dart",
}

LANG_DISPLAY_NAME = {
    "python": "Python",
    "python3": "Python 3",
    "pythondata": "Python (Pandas)",
    "pythonml": "Python (ML)",
    "c": "C",
    "cpp": "C++",
    "csharp": "C#",
    "java": "Java",
    "kotlin": "Kotlin",
    "mysql": "MySQL",
    "mssql": "MS SQL",
    "oraclesql": "Oracle SQL",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "html": "HTML",
    "php": "PHP",
    "golang": "Go",
    "scala": "Scala",
    "rust": "Rust",
    "ruby": "Ruby",
    "bash": "Bash",
    "swift": "Swift",
    "elixir": "Elixir",
    "erlang": "Erlang",
    "racket": "Racket",
    "dart": "Dart",
}


def lang_to_ext(lang: str) -> str:
    return LANG_TO_EXTENSION.get(lang, lang)


def lang_display(lang: str) -> str:
    return LANG_DISPLAY_NAME.get(lang, lang.capitalize())


def load_cookies(explicit: Optional[str] = None, repo_root: str = ".") -> str:
    """Resolve cookies from CLI arg, env var, file, or interactive prompt."""
    if explicit:
        return explicit.strip()

    env_val = os.environ.get("LEETCODE_COOKIES")
    if env_val:
        return env_val.strip()

    cookie_file = os.path.join(repo_root, ".leetcode_cookies")
    if os.path.isfile(cookie_file):
        with open(cookie_file, "r", encoding="utf-8") as f:
            return f.read().strip()

    if sys.stdin.isatty():
        print(
            "No cookies found. Paste your LeetCode cookie header below.\n"
            "(Open leetcode.com in a browser, open DevTools, go to Network, click any "
            "leetcode.com request, then copy the entire 'cookie' request header.)"
        )
        return input("Cookies: ").strip()

    raise RuntimeError(
        "No LeetCode cookies provided. Pass --cookies, set LEETCODE_COOKIES, "
        "or create a .leetcode_cookies file in the repo root."
    )


class LeetCodeClient:
    def __init__(self, cookies: str, request_delay: float = 2.0):
        self.session = requests.Session()
        self.session.headers.update(REQUEST_HEADERS)
        self.request_delay = request_delay
        self._authenticated = False
        if not self._set_cookies(cookies):
            raise RuntimeError(
                "Cookies are not valid or expired. Get a fresh cookie header "
                "from your browser's Network tab."
            )

    def _set_cookies(self, cookies: str) -> bool:
        cookie_dict: Dict[str, str] = {}
        for cookie in cookies.split(";"):
            parts = [p.strip() for p in cookie.split("=", 1)]
            if len(parts) != 2:
                continue
            cookie_dict[parts[0]] = parts[1]

        if "csrftoken" not in cookie_dict or "LEETCODE_SESSION" not in cookie_dict:
            logging.error(
                "Cookie string must contain both csrftoken and LEETCODE_SESSION."
            )
            return False

        for k, v in cookie_dict.items():
            self.session.cookies.set(k, v)

        # Set csrf token in headers too (required for some endpoints).
        self.session.headers["X-CSRFToken"] = cookie_dict["csrftoken"]
        self.session.headers["X-Requested-With"] = "XMLHttpRequest"

        return self._verify_login()

    def _verify_login(self) -> bool:
        resp = self.session.get(SUBMISSIONS_API_URL.format(0, 1))
        sleep(1)
        try:
            data = resp.json()
        except ValueError:
            logging.error("Login check returned non-JSON. Body: %s", resp.text[:200])
            return False
        if "detail" in data:
            logging.error("Login failed: %s", data.get("detail"))
            return False
        self._authenticated = True
        logging.info("LeetCode login OK")
        return True

    def iter_submissions(
        self,
        stop_at_timestamp: Optional[int] = None,
        page_size: int = 20,
    ) -> Iterator[Dict]:
        """Yield raw submission dicts in reverse chronological order.

        If stop_at_timestamp is given, stops as soon as a submission with
        timestamp <= stop_at_timestamp is encountered (the LeetCode API returns
        submissions newest-first, so this is safe for incremental sync).
        """
        offset = 0
        while True:
            url = SUBMISSIONS_API_URL.format(offset, page_size)
            logging.debug("GET %s", url)
            resp = self.session.get(url)
            try:
                data = resp.json()
            except ValueError:
                logging.error("Non-JSON response at offset %d: %s", offset, resp.text[:200])
                return

            if "detail" in data:
                logging.warning("LeetCode API error: %s", data["detail"])
                return

            dump = data.get("submissions_dump", [])
            if not dump:
                return

            for sub in dump:
                if stop_at_timestamp is not None and sub.get("timestamp", 0) <= stop_at_timestamp:
                    return
                yield self._normalize_submission(sub)

            if not data.get("has_next", False):
                return

            offset += page_size
            sleep(self.request_delay)

    @staticmethod
    def _normalize_submission(sub: Dict) -> Dict:
        sub = dict(sub)
        sub["runtime"] = (sub.get("runtime") or "").replace(" ", "")
        sub["memory"] = (sub.get("memory") or "").replace(" ", "")
        ts = sub.get("timestamp", 0)
        sub["date_formatted"] = datetime.datetime.fromtimestamp(ts).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        sub["extension"] = lang_to_ext(sub.get("lang", ""))
        return sub

    def get_problem_metadata(self, slug: str) -> Optional[Dict]:
        """Fetch metadata only (NO description content) for a problem.

        We deliberately omit `content` from the GraphQL query to avoid
        accidentally storing copyrighted problem statements.
        """
        query = """
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                title
                titleSlug
                difficulty
                isPaidOnly
                likes
                dislikes
                stats
                topicTags { name slug }
                similarQuestions
            }
        }
        """
        payload = {
            "operationName": "getQuestionDetail",
            "variables": {"titleSlug": slug},
            "query": query,
        }
        resp = self.session.post(GRAPHQL_URL, json=payload)
        sleep(self.request_delay / 2)
        try:
            data = resp.json()
        except ValueError:
            logging.error("Non-JSON GraphQL response for %s", slug)
            return None
        question = (data.get("data") or {}).get("question")
        if not question:
            logging.warning("No metadata returned for slug=%s", slug)
            return None

        # Parse the embedded stats JSON string.
        stats_raw = question.get("stats")
        if isinstance(stats_raw, str):
            try:
                question["stats_parsed"] = json.loads(stats_raw)
            except json.JSONDecodeError:
                question["stats_parsed"] = {}
        else:
            question["stats_parsed"] = stats_raw or {}

        # Parse similarQuestions (also a JSON-encoded string).
        sim_raw = question.get("similarQuestions")
        if isinstance(sim_raw, str) and sim_raw:
            try:
                question["similar_parsed"] = json.loads(sim_raw)
            except json.JSONDecodeError:
                question["similar_parsed"] = []
        else:
            question["similar_parsed"] = []

        return question
