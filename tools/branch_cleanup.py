# /// script
# requires-python = ">=3.10"
# ///
"""Branch cleanup: delete every branch of one repository that is not ahead of its default branch.

R-WS-014 (DESIGN-28). Run inside GitHub Actions by .github/workflows/branch-cleanup.yml with the repository's own
token, because a cloud session gets HTTP 403 when it deletes a branch (CONSTRAINT-9). A branch is kept, with its
reason, when it is the default branch, protected, on the keep list, the head of an open pull request of this
repository, ahead of the default branch, or without history in common with it. Every other branch is deleted. The
run lists each deleted branch with its last commit, which the default branch holds, so the branch can be made again:

    git push origin <commit>:refs/heads/<branch>

Usage, with the token in GH_TOKEN or GITHUB_TOKEN (never printed):

    python tools/branch_cleanup.py --repo e1-rahabok/agent-e2 --dry-run
    python tools/branch_cleanup.py --repo e1-rahabok/PCM-Adapter --keep badges

tools/test_branch_cleanup.py runs it against a fake GitHub (T-WS-014a).
Exit 0: done. Exit 1: GitHub refused a call; the run names it.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Callable, Iterator

API = "https://api.github.com"
PAGE = 100


class GitHubError(Exception):
    def __init__(self, status: int, path: str, message: str):
        super().__init__(f"{status} on {path}")
        self.status, self.path, self.message = status, path, message


class GitHub:
    """The few REST calls the cleanup makes."""

    def __init__(self, credential: str):
        self._credential = credential

    def _call(self, method: str, path: str):
        request = urllib.request.Request(API + path, method=method, headers={
            "Authorization": f"Bearer {self._credential}", "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "branch-cleanup"})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read()
                return json.loads(body) if body else None
        except urllib.error.HTTPError as e:
            raise GitHubError(e.code, path, e.read().decode("utf-8", "replace")[:300]) from None

    def get(self, path: str):
        return self._call("GET", path)

    def delete(self, path: str):
        return self._call("DELETE", path)


@dataclass
class Decision:
    branch: str
    commit: str
    delete: bool
    reason: str


def ref(name: str) -> str:
    return urllib.parse.quote(name, safe="/")


def pages(gh, path: str) -> Iterator[dict]:
    page = 1
    while True:
        joiner = "&" if "?" in path else "?"
        batch = gh.get(f"{path}{joiner}per_page={PAGE}&page={page}") or []
        yield from batch
        if len(batch) < PAGE:
            return
        page += 1


def decide(gh, repo: str, keep: set[str]) -> list[Decision]:
    default = gh.get(f"/repos/{repo}")["default_branch"]
    open_heads = {p["head"]["ref"] for p in pages(gh, f"/repos/{repo}/pulls?state=open")
                  if ((p.get("head") or {}).get("repo") or {}).get("full_name") == repo}
    decisions = []
    for b in pages(gh, f"/repos/{repo}/branches"):
        name, commit = b["name"], b["commit"]["sha"]

        def kept(reason: str) -> None:
            decisions.append(Decision(name, commit, False, reason))

        if name == default:
            kept("the default branch")
        elif name in keep:
            kept("on the keep list")
        elif b.get("protected"):
            kept("protected")
        elif name in open_heads:
            kept("the head of an open pull request")
        else:
            try:
                compare = gh.get(f"/repos/{repo}/compare/{ref(default)}...{ref(name)}")
            except GitHubError as e:
                if e.status == 404 and "common ancestor" in e.message.lower():
                    kept(f"no history in common with {default}")
                    continue
                raise
            ahead = compare["ahead_by"]
            if ahead:
                kept(f"{ahead} commit{'s' if ahead != 1 else ''} ahead of {default}")
            else:
                decisions.append(Decision(name, commit, True, f"0 commits ahead of {default}"))
    return decisions


def run(gh, repo: str, keep: set[str], dry_run: bool, out: Callable[[str], None]) -> int:
    try:
        decisions = decide(gh, repo, keep)
    except GitHubError as e:
        out(f"FAIL GitHub answered {e.status} on {e.path}")
        return 1
    failed = deleted = 0
    for d in decisions:
        if not d.delete:
            out(f"KEEP {d.branch}: {d.reason}")
        elif dry_run:
            out(f"WOULD DELETE {d.branch} at {d.commit}: {d.reason}")
        else:
            try:
                gh.delete(f"/repos/{repo}/git/refs/heads/{ref(d.branch)}")
            except GitHubError as e:
                if e.status == 422 and "does not exist" in e.message.lower():
                    out(f"GONE {d.branch}: already deleted")
                    continue
                out(f"FAIL {d.branch}: GitHub answered {e.status} to the deletion")
                failed += 1
                continue
            deleted += 1
            out(f"DELETED {d.branch} at {d.commit}: {d.reason}")
    to_delete = sum(d.delete for d in decisions)
    if dry_run:
        out(f"Branch cleanup of {repo} (dry run): {to_delete} to delete, {len(decisions) - to_delete} kept")
    else:
        out(f"Branch cleanup of {repo}: {deleted} deleted, {len(decisions) - to_delete} kept, {failed} refused")
    return 1 if failed else 0


def annotate(lines: list[str]) -> None:
    """One notice with every line, readable from the check run's annotations, and the job summary."""
    text = "\n".join(lines)
    escaped = text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    print(f"::notice title=Branch cleanup::{escaped}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("## Branch cleanup\n\n" + "".join(f"- {line}\n" for line in lines))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", required=True, help="owner/name")
    parser.add_argument("--keep", default="", help="branches to keep, separated by commas or spaces")
    parser.add_argument("--dry-run", action="store_true", help="list what would be deleted, delete nothing")
    args = parser.parse_args()
    credential = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not credential:
        print("FAIL no token in GH_TOKEN or GITHUB_TOKEN")
        return 1
    keep = {k for k in re.split(r"[,\s]+", args.keep) if k}
    lines: list[str] = []

    def out(line: str) -> None:
        print(line)
        lines.append(line)

    code = run(GitHub(credential), args.repo, keep, args.dry_run, out)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        annotate(lines)
    return code


if __name__ == "__main__":
    sys.exit(main())
