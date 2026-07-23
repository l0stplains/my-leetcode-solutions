import os
import sys
import tempfile
import unittest


SCRIPTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "scripts")
)
sys.path.insert(0, SCRIPTS_DIR)

import commit_sync


class CommitSyncTests(unittest.TestCase):
    def test_writes_unique_scoped_paths_with_main_readme_first(self):
        with tempfile.TemporaryDirectory() as directory:
            output = os.path.join(directory, "paths")
            commit_sync.write_sync_paths(
                [
                    "problems/560-subarray-sum-equals-k",
                    "README.md",
                    "problems/122-best-time-to-buy-and-sell-stock-ii",
                    "README.md",
                ],
                output,
            )
            with open(output, "r", encoding="utf-8") as file:
                paths = file.read().splitlines()

        self.assertEqual(
            paths,
            [
                "README.md",
                "problems/122-best-time-to-buy-and-sell-stock-ii",
                "problems/560-subarray-sum-equals-k",
            ],
        )

    def test_rejects_paths_outside_generated_solution_scope(self):
        for path in (".gitignore", "scripts/sync_submissions.py", "../README.md"):
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    commit_sync.validate_sync_path(path)

    def test_detects_files_inside_a_recorded_problem_folder(self):
        scopes = ["README.md", "problems/122-best-time-to-buy-and-sell-stock-ii"]
        self.assertTrue(commit_sync.is_in_scope("README.md", scopes))
        self.assertTrue(
            commit_sync.is_in_scope(
                "problems/122-best-time-to-buy-and-sell-stock-ii/solution.java",
                scopes,
            )
        )
        self.assertFalse(
            commit_sync.is_in_scope("scripts/sync_submissions.py", scopes)
        )


if __name__ == "__main__":
    unittest.main()
