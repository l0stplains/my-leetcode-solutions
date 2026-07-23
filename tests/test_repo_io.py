import os
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "scripts")
)
sys.path.insert(0, SCRIPTS_DIR)

import repo_io


class FindExistingProblemFolderTests(unittest.TestCase):
    def test_matches_the_complete_slug_not_a_suffix(self):
        with tempfile.TemporaryDirectory() as problems_dir:
            min_cost = os.path.join(problems_dir, "746-min-cost-climbing-stairs")
            climbing = os.path.join(problems_dir, "70-climbing-stairs")
            os.makedirs(min_cost)
            os.makedirs(climbing)

            with mock.patch.object(repo_io, "PROBLEMS_DIR", problems_dir):
                self.assertEqual(
                    repo_io.find_existing_problem_folder("climbing-stairs"),
                    climbing,
                )
                self.assertEqual(
                    repo_io.find_existing_problem_folder(
                        "min-cost-climbing-stairs"
                    ),
                    min_cost,
                )


class WriteProblemReadmeTests(unittest.TestCase):
    def test_preserves_last_updated_when_using_cached_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            readme_path = os.path.join(folder, "README.md")
            with open(readme_path, "w", encoding="utf-8") as file:
                file.write("> *Last updated: 2026-05-26 10:53:03*\n")

            metadata = {
                "questionFrontendId": "1",
                "title": "Two Sum",
                "titleSlug": "two-sum",
                "difficulty": "Easy",
                "topicTags": [],
                "stats_parsed": {"acRate": "50%"},
            }
            repo_io.write_problem_readme(folder, metadata, {}, [])

            with open(readme_path, "r", encoding="utf-8") as file:
                rendered = file.read()

        self.assertIn(
            "> *Last updated: 2026-05-26 10:53:03*",
            rendered,
        )


if __name__ == "__main__":
    unittest.main()
