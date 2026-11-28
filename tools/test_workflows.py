"""Planted breaks for tools/workflows.py (R-WS-012, T-WS-012a and T-WS-012c; R-WS-014, T-WS-014b). Run: python -m unittest discover -s tools -p "test_*.py"."""
import subprocess
import tempfile
import unittest
from pathlib import Path

import workflows as wf

GOOD_WORKFLOW = """name: ci
on: [pull_request]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      # - uses: someone/commented-out@v1
      - uses: pnpm/action-setup@0123456789abcdef0123456789abcdef01234567
  shared:
    uses: e1-rahabok/private-cloud-workspace/.github/workflows/cross-repo.yml@main
  branch-cleanup:
    uses: e1-rahabok/private-cloud-workspace/.github/workflows/branch-cleanup.yml@main
"""
DEPENDABOT = """version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule: {interval: weekly}
"""


def clone_with(files: dict[str, str]) -> tempfile.TemporaryDirectory:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    return tmp


class PlantedWorkflows(unittest.TestCase):
    def test_a_good_repository_passes(self):
        with clone_with({".github/workflows/ci.yml": GOOD_WORKFLOW, ".github/dependabot.yml": DEPENDABOT}) as tmp:
            self.assertEqual(wf.problems_in("agent-e2", Path(tmp)), [])

    def test_no_permissions_fails(self):
        text = GOOD_WORKFLOW.replace("permissions:\n  contents: read\n", "")
        with clone_with({".github/workflows/ci.yml": text, ".github/dependabot.yml": DEPENDABOT}) as tmp:
            problems = wf.problems_in("agent-e2", Path(tmp))
        self.assertEqual(len(problems), 1)
        self.assertIn("no top-level permissions", problems[0])

    def test_a_third_party_action_on_a_tag_fails(self):
        text = GOOD_WORKFLOW.replace("  shared:\n", "      - uses: tj-actions/changed-files@v45\n  shared:\n")
        with clone_with({".github/workflows/ci.yml": text, ".github/dependabot.yml": DEPENDABOT}) as tmp:
            problems = wf.problems_in("agent-e2", Path(tmp))
        self.assertEqual(len(problems), 1)
        self.assertIn("tj-actions/changed-files@v45", problems[0])

    def test_a_missing_dependabot_or_ecosystem_fails(self):
        with clone_with({".github/workflows/ci.yml": GOOD_WORKFLOW}) as tmp:
            self.assertIn("dependabot.yml is missing", wf.problems_in("agent-e2", Path(tmp))[0])
        with clone_with({".github/workflows/ci.yml": GOOD_WORKFLOW, ".github/dependabot.yml": DEPENDABOT,
                         "package-lock.json": "{}", "app/requirements.txt": "requests==2.32.3\n"}) as tmp:
            problems = wf.problems_in("isvara", Path(tmp))
        self.assertEqual(sorted(p.split(" has no ")[1].split(" entry")[0] for p in problems), ["npm", "pip"])

    def test_a_workflow_that_holds_the_gateway_key_fails(self):
        text = GOOD_WORKFLOW.replace("      - uses: actions/setup-node@v4\n",
                                    "      - uses: actions/setup-node@v4\n      - run: python3 benchmark/runner/round_executor.py\n"
                                    "        env:\n          AI_GATEWAY_API_KEY: ${{ secrets.AI_GATEWAY_API_KEY }}\n")
        with clone_with({".github/workflows/ci.yml": text, ".github/dependabot.yml": DEPENDABOT}) as tmp:
            problems = wf.problems_in("agent-e2", Path(tmp))
        self.assertEqual(len(problems), 1, problems)                    # one problem per line that names the key
        self.assertIn("names AI_GATEWAY_API_KEY", problems[0])
        with clone_with({".github/workflows/ci.yml": GOOD_WORKFLOW.replace("# - uses", "# AI_GATEWAY_API_KEY - uses"),
                         ".github/dependabot.yml": DEPENDABOT}) as tmp:
            self.assertEqual(wf.problems_in("agent-e2", Path(tmp)), [])  # a comment is not a key

    def test_a_repository_without_the_branch_cleanup_fails(self):
        text = GOOD_WORKFLOW.split("  branch-cleanup:\n")[0]
        with clone_with({".github/workflows/ci.yml": text, ".github/dependabot.yml": DEPENDABOT}) as tmp:
            problems = wf.problems_in("isvara", Path(tmp))
        self.assertEqual(len(problems), 1)
        self.assertIn("no workflow calls the branch cleanup", problems[0])

    def test_the_workspace_passes_with_its_own_branch_cleanup_and_a_child_does_not(self):
        text = GOOD_WORKFLOW.split("  branch-cleanup:\n")[0]
        files = {".github/workflows/ci.yml": text, ".github/workflows/branch-cleanup.yml": text,
                 ".github/dependabot.yml": DEPENDABOT}
        with clone_with(files) as tmp:
            self.assertEqual(wf.problems_in("private-cloud-workspace", Path(tmp)), [])
            self.assertEqual(len(wf.problems_in("agent-e2", Path(tmp))), 1)


if __name__ == "__main__":
    unittest.main()
