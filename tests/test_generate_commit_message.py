import json
import os
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "scripts")
)
sys.path.insert(0, SCRIPTS_DIR)

import generate_commit_message


class GenerateCommitMessageTests(unittest.TestCase):
    def test_summarizes_meaningful_changes_and_collapses_readme_churn(self):
        with tempfile.TemporaryDirectory() as repo:
            previous_directory = os.getcwd()
            os.chdir(repo)
            try:
                os.makedirs("problems/122-best-time-to-buy-and-sell-stock-ii")
                with open(
                    "problems/122-best-time-to-buy-and-sell-stock-ii/.meta.json",
                    "w",
                    encoding="utf-8",
                ) as file:
                    json.dump(
                        {
                            "questionFrontendId": "122",
                            "title": "Best Time to Buy and Sell Stock II",
                        },
                        file,
                    )

                status = [
                    ("??", "problems/122-best-time-to-buy-and-sell-stock-ii/.meta.json"),
                    ("??", "problems/122-best-time-to-buy-and-sell-stock-ii/solution.java"),
                    (" M", "problems/1480-running-sum-of-1d-array/solution.cpp"),
                    (" M", "problems/1-two-sum/README.md"),
                    (" M", "README.md"),
                ]
                tracked = {
                    "1-two-sum",
                    "1480-running-sum-of-1d-array",
                }

                with mock.patch.object(
                    generate_commit_message, "parse_status", return_value=status
                ), mock.patch.object(
                    generate_commit_message,
                    "tracked_problem_folders",
                    return_value=tracked,
                ):
                    message = generate_commit_message.generate_commit_message()
            finally:
                os.chdir(previous_directory)

        self.assertEqual(
            message,
            (
                "feat(solutions): sync 2 LeetCode solutions\n"
                "\n"
                "- Add #122 Best Time to Buy and Sell Stock II (Java)\n"
                "- Update #1480 Running Sum Of 1D Array (C++)\n"
                "- Refresh generated problem documentation and solution index\n"
            ),
        )


if __name__ == "__main__":
    unittest.main()
