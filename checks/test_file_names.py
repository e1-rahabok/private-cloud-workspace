"""Planted breaks for checks/file_names.py (R-WS-007, T-WS-007a). Run: python -m unittest discover -s checks -p "test_*.py"."""
import unittest

import file_names as names


class PlantedNames(unittest.TestCase):
    def test_a_version_or_milestone_in_a_name_fails(self):
        problems = names.problems_in("private-cloud-manager", ["docs/report_v2.md", "build/tests/story_m5.py"])
        self.assertEqual(len(problems), 2, problems)

    def test_a_status_word_in_a_folder_fails_once(self):
        problems = names.problems_in("isvara", ["lib/old/a.ts", "lib/old/b.ts", "app/proto-page.tsx"])
        self.assertEqual(problems, ["isvara: 'app/proto-page.tsx' holds 'proto'", "isvara: 'lib/old' holds 'old'"])

    def test_titles_review_pages_and_words_inside_words_pass(self):
        paths = ["knowledge/sp5-framework/why-a-new-framework.md", "spec/review/M9.md",
                 "knowledge/catalog/thresholds-performance.yaml", "docs/version-history.md", "lib/newsletter.ts"]
        self.assertEqual(names.problems_in("agent-e2", paths), [])
        self.assertEqual(names.problems_in("private-cloud-workspace", ["spec/review/M9.md"]), [])

    def test_a_title_folder_is_exempt_only_in_its_repository(self):
        self.assertEqual(names.problems_in("agent-e2", ["knowledge/old-notes.md"]), [])
        self.assertEqual(len(names.problems_in("isvara", ["knowledge/old-notes.md"])), 1)


if __name__ == "__main__":
    unittest.main()
