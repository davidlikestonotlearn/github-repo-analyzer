
import unittest
from main import count_languages, find_popular_repo, rank_repositories


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.repos = [
            {"name": "one", "stargazers_count": 2, "language": "Python"},
            {"name": "two", "stargazers_count": 8, "language": "JavaScript"},
            {"name": "three", "stargazers_count": 1, "language": "Python"},
            {"name": "four", "stargazers_count": 0, "language": None},
        ]

    def test_popular_repo(self):
        self.assertEqual(find_popular_repo(self.repos)["name"], "two")
        self.assertIsNone(find_popular_repo([]))

    def test_ranking(self):
        self.assertEqual(
            [r["name"] for r in rank_repositories(self.repos)],
            ["two", "one", "three", "four"]
        )

    def test_languages(self):
        self.assertEqual(count_languages(self.repos)["Python"], 2)
        self.assertNotIn(None, count_languages(self.repos))


if __name__ == "__main__":
    unittest.main()
