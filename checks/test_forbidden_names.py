"""Planted breaks for checks/forbidden_names.py (R-REPO-006, T-REPO-006a; R-REPO-007 and R-REPO-008, T-REPO-007b, T-REPO-008e). Run: python -m unittest discover -s checks -p "test_*.py"."""
import subprocess
import tempfile
import unittest
from pathlib import Path

import forbidden_names as names


def clone_with(files: dict[str, str]) -> tempfile.TemporaryDirectory:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    return tmp


class PlantedOldNames(unittest.TestCase):
    def test_an_old_name_fails_and_names_the_line(self):
        with clone_with({"README.md": "See https://github.com/e1-rahabok/VCF-vCommunity-Adapter\n",
                         "docs/a.md": "fine\nPrivate-Cloud-Management repo\n"}) as tmp:
            problems = names.problems_in("isvara", Path(tmp))
        self.assertEqual(sorted(p.split(" names")[0] for p in problems), ["isvara: README.md:1", "isvara: docs/a.md:2"])

    def test_an_old_pcm_path_fails(self):
        with clone_with({"docs/x.md": "run python3 -m build.pcm_proto.server\n",
                         "SYSTEM.md": "[t](https://github.com/e1-rahabok/private-cloud-manager/tree/main/build/tests)\n",
                         "b.py": "from tests import test_story_m5\n"}) as tmp:
            problems = names.problems_in("agent-e2", Path(tmp))
        self.assertEqual(sorted(p.rsplit("(", 1)[1] for p in problems), ["R-REPO-007)", "R-REPO-007)", "R-REPO-008)"])

    def test_an_old_pcm_path_written_out_fails_and_a_new_one_passes(self):
        with clone_with({"ARCHITECTURE.md": "PCM `spec/workspaces/l2/frame.md`\n",
                         "live.md": "no change under spec/tests/ and build/tests/\n",
                         "new.md": "see pcm/core/spec/catalog/settings.yaml and pcm/l2/spec/pages/frame.md\n"}) as tmp:
            problems = names.problems_in("agent-e2", Path(tmp))
        self.assertEqual(sorted(p.split(":")[1].strip() for p in problems), ["ARCHITECTURE.md", "live.md"])

    def test_a_link_pinned_to_a_commit_and_the_tutorial_pass(self):
        with clone_with({"README.md": "[b](https://github.com/e1-rahabok/private-cloud-manager/blob/69a3928/build/README.md)\n",
                         "tutorial/10.md": "`pcm_proto` stops being true\n"}) as tmp:
            self.assertEqual(names.problems_in("private-cloud-workspace", Path(tmp)), [])

    def test_files_that_forbid_the_names_pass(self):
        with clone_with({"spec/requirements/x.md": "no VCF-vCommunity-Adapter\n",
                         "DECISIONS.md": "private-cloud-management was renamed\n"}) as tmp:
            self.assertEqual(names.problems_in("private-cloud-workspace", Path(tmp)), [])

    def test_the_product_name_passes(self):
        with clone_with({"README.md": "Private Cloud Management, the discipline; VCF vCommunity Adapter\n"}) as tmp:
            self.assertEqual(names.problems_in("isvara", Path(tmp)), [])


if __name__ == "__main__":
    unittest.main()
