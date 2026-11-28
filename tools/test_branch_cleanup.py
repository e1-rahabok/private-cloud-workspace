"""Planted cases for tools/branch_cleanup.py against a fake GitHub (R-WS-014, T-WS-014a). Run: python -m unittest discover -s tools -p "test_*.py"."""
import unittest

import branch_cleanup as cleanup

REPO = "e1-rahabok/example"
SHA = "a" * 40


class FakeGitHub:
    """Answers the cleanup's calls from tables; records every deletion."""

    def __init__(self, branches, ahead=None, pulls=(), refuse=(), gone=(), fail_on=None):
        self.branches = branches  # list of (name, protected)
        self.ahead = ahead or {}  # name -> commits ahead of main, or None for no common history
        self.pulls = list(pulls)  # list of (head ref, head repo)
        self.refuse, self.gone, self.fail_on = set(refuse), set(gone), fail_on
        self.deleted = []

    def get(self, path):
        if self.fail_on and path.startswith(self.fail_on):
            raise cleanup.GitHubError(403, path, "Resource not accessible by integration")
        if path == f"/repos/{REPO}":
            return {"default_branch": "main"}
        page = int(path.rsplit("page=", 1)[1]) if "page=" in path else 1
        if path.startswith(f"/repos/{REPO}/pulls?"):
            rows = [{"head": {"ref": r, "repo": {"full_name": owner}}} for r, owner in self.pulls]
            return rows[(page - 1) * 100:page * 100]
        if path.startswith(f"/repos/{REPO}/branches?"):
            rows = [{"name": n, "protected": p, "commit": {"sha": SHA}} for n, p in self.branches]
            return rows[(page - 1) * 100:page * 100]
        if path.startswith(f"/repos/{REPO}/compare/main..."):
            name = path.split("...", 1)[1]
            ahead = self.ahead.get(name, 0)
            if ahead is None:
                raise cleanup.GitHubError(404, path, '{"message":"No common ancestor between main and x."}')
            return {"ahead_by": ahead, "status": "ahead" if ahead else "behind"}
        raise AssertionError(f"unexpected call {path}")

    def delete(self, path):
        name = path.split("/git/refs/heads/", 1)[1]
        if name in self.refuse:
            raise cleanup.GitHubError(403, path, "Resource not accessible by integration")
        if name in self.gone:
            raise cleanup.GitHubError(422, path, '{"message":"Reference does not exist"}')
        self.deleted.append(name)


def run(gh, keep=(), dry_run=False):
    lines = []
    code = cleanup.run(gh, REPO, set(keep), dry_run, lines.append)
    return code, lines


class BranchCleanup(unittest.TestCase):
    def test_a_branch_not_ahead_of_main_is_deleted_and_listed_with_its_commit(self):
        gh = FakeGitHub([("main", True), ("claude/old-session", False), ("docs/merged", False)])
        code, lines = run(gh)
        self.assertEqual(code, 0)
        self.assertEqual(gh.deleted, ["claude/old-session", "docs/merged"])
        self.assertIn(f"DELETED claude/old-session at {SHA}: 0 commits ahead of main", lines)

    def test_each_kind_to_keep_is_kept_with_its_reason(self):
        gh = FakeGitHub(
            [("main", False), ("badges", False), ("release", True), ("open-work", False), ("ahead", False),
             ("one-ahead", False), ("orphan", False)],
            ahead={"ahead": 2, "one-ahead": 1, "orphan": None, "badges": None},
            pulls=[("open-work", REPO)])
        code, lines = run(gh, keep=["badges"])
        self.assertEqual(code, 0)
        self.assertEqual(gh.deleted, [])
        self.assertEqual(lines[:7], [
            "KEEP main: the default branch",
            "KEEP badges: on the keep list",
            "KEEP release: protected",
            "KEEP open-work: the head of an open pull request",
            "KEEP ahead: 2 commits ahead of main",
            "KEEP one-ahead: 1 commit ahead of main",
            "KEEP orphan: no history in common with main",
        ])

    def test_an_open_pull_request_from_a_fork_does_not_keep_a_branch_of_the_same_name(self):
        gh = FakeGitHub([("main", True), ("fix", False)], pulls=[("fix", "someone/fork")])
        run(gh)
        self.assertEqual(gh.deleted, ["fix"])

    def test_a_dry_run_deletes_nothing_and_lists_what_it_would_delete(self):
        gh = FakeGitHub([("main", True), ("old", False), ("ahead", False)], ahead={"ahead": 3})
        code, lines = run(gh, dry_run=True)
        self.assertEqual(code, 0)
        self.assertEqual(gh.deleted, [])
        self.assertIn(f"WOULD DELETE old at {SHA}: 0 commits ahead of main", lines)
        self.assertEqual(lines[-1], f"Branch cleanup of {REPO} (dry run): 1 to delete, 2 kept")

    def test_a_refused_deletion_fails_the_run_and_the_rest_go_on(self):
        gh = FakeGitHub([("main", True), ("stuck", False), ("old", False)], refuse=["stuck"])
        code, lines = run(gh)
        self.assertEqual(code, 1)
        self.assertEqual(gh.deleted, ["old"])
        self.assertIn("FAIL stuck: GitHub answered 403 to the deletion", lines)

    def test_a_branch_deleted_meanwhile_does_not_fail_the_run(self):
        gh = FakeGitHub([("main", True), ("raced", False)], gone=["raced"])
        code, lines = run(gh)
        self.assertEqual(code, 0)
        self.assertIn("GONE raced: already deleted", lines)

    def test_a_refused_read_fails_the_run_and_deletes_nothing(self):
        gh = FakeGitHub([("main", True), ("old", False)], fail_on=f"/repos/{REPO}/pulls")
        code, lines = run(gh)
        self.assertEqual(code, 1)
        self.assertEqual(gh.deleted, [])
        self.assertTrue(lines[0].startswith("FAIL GitHub answered 403"))

    def test_every_page_of_branches_is_read(self):
        names = [f"old-{i:03}" for i in range(150)]
        gh = FakeGitHub([("main", True)] + [(n, False) for n in names])
        run(gh)
        self.assertEqual(gh.deleted, names)

    def test_a_branch_name_with_a_special_character_is_quoted_in_the_path(self):
        self.assertEqual(cleanup.ref("docs/a b#1"), "docs/a%20b%231")


if __name__ == "__main__":
    unittest.main()
