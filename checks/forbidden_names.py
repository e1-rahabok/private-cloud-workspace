# /// script
# requires-python = ">=3.10"
# ///
"""Check of forbidden names: no repository uses an old repository name or one of PCM's old paths.

Each rule searches the tracked text files of every clone and fails on a line that matches it, outside the files
that name the old names to forbid them, give them as examples, or record them as they were (OUTSIDE below):
- R-REPO-006 (Q-WS-3, WD-007, WD-028): the old repository names "VCF-vCommunity-Adapter" and
  "private-cloud-management", in any case.
- R-REPO-007 and R-REPO-008 (T-REPO-007b, T-REPO-008e): PCM's old package and file names `pcm_proto` and `story_m5`,
  links to PCM's old folders `build/` and `sources/` on its main branch, and PCM's old paths written out
  (`build/tests`, `build/pcm_proto`, and `spec/<folder>/` for the specification folders that moved into each
  workspace in D-133). A link pinned to a commit, as the interview records use, still resolves and is not an old
  name; a path inside a workspace folder, such as `pcm/core/spec/catalog/`, is a new path.

Outside every rule: decision logs, the interview records, agent-e2's record of the author's answers, the adapter's
dated engineering reviews, the workspace's tutorial (it gives the old names as examples) and these checks' own planted
breaks. Outside R-REPO-006 also: every requirement file and review page, which name the old repository names to forbid
them. Outside R-REPO-007 and R-REPO-008 also: only the requirement files that forbid PCM's old paths; any other
requirement file that links an old path fails, as T-REPO-008e asks.

A repository with no clone is reported as not run: isvara is private, so the workspace's CI cannot read it, and
isvara's own CI runs this check (R-WS-002). checks/test_forbidden_names.py plants a break of each kind and expects a failure.
Exit 0: no problem. Exit 1: a problem. Exit 2: no repository could be read.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPOS = ["private-cloud-workspace", "agent-e2", "PCM-Adapter", "private-cloud-manager", "isvara"]
# Each rule: its requirement, its pattern, and the path prefixes outside its search per repository ("*": every one).
RECORDS = {
    "private-cloud-workspace": ["DECISIONS.md", "spec/interview-round-", "tutorial/", "checks/forbidden_names.py",
                                "checks/test_forbidden_names.py", "checks/test_file_names.py"],
    "agent-e2": ["project/author-questions-resolved.md"],
    "PCM-Adapter": ["docs/development-guide/engineering-review/"],
    "private-cloud-manager": ["decisions.md"],
}
RULES = [
    ("R-REPO-006", re.compile(r"VCF-vCommunity-Adapter|private-cloud-management", re.IGNORECASE),
     {"*": ["spec/requirements/", "project/requirements/"], "private-cloud-workspace": ["spec/review/"]}),
    ("R-REPO-007", re.compile(r"pcm_proto|story_m5"),
     {"private-cloud-workspace": ["spec/requirements/workspace.md", "spec/review/"],
      "private-cloud-manager": ["spec/requirements/clean-up.md"]}),
    ("R-REPO-008", re.compile(r"private-cloud-manager/(?:blob|tree)/main/(?:build|sources)(?:/|\b)"
                              r"|(?<![\w/-])build/(?:tests|pcm_proto)\b"
                              r"|(?<![\w/-])spec/(?:workspaces|catalog|data|design-system|api|objects|database|tests)/"),
     {"private-cloud-manager": ["spec/requirements/clean-up.md"]}),
]
# What git grep reads first, in its own pattern language; the rules above then decide.
PREFILTER = (r"VCF-vCommunity-Adapter|private-cloud-management|pcm_proto|story_m5|private-cloud-manager/(blob|tree)/main/(build|sources)"
             r"|build/(tests|pcm_proto)|spec/(workspaces|catalog|data|design-system|api|objects|database|tests)/")


def outside(repo: str, path: str, rule_outside: dict[str, list[str]]) -> bool:
    prefixes = RECORDS.get(repo, []) + rule_outside.get("*", []) + rule_outside.get(repo, [])
    return any(path.startswith(p) for p in prefixes)


def problems_in(repo: str, clone: Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(clone), "grep", "-I", "-n", "-i", "-E", PREFILTER],
                         capture_output=True, text=True).stdout
    problems = []
    for line in out.split("\n"):
        if not line or line.count(":") < 2:
            continue
        path, number, text = line.split(":", 2)
        for requirement, rule, rule_outside in RULES:
            m = rule.search(text)
            if m and not outside(repo, path, rule_outside):
                problems.append(f"{repo}: {path}:{number} names '{m.group(0)}' ({requirement})")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repos", type=Path, default=Path(__file__).resolve().parents[2],
                        help="folder that holds the clones (default: next to this repository)")
    args = parser.parse_args()
    problems, read, not_run = [], 0, []
    for repo in REPOS:
        clone = args.repos / repo
        if not (clone / ".git").exists():
            not_run.append(repo)
            continue
        read += 1
        problems += problems_in(repo, clone)
    for repo in not_run:
        print(f"NOT RUN {repo}: no clone")
    for p in problems:
        print(f"FAIL {p}")
    print(f"Forbidden names: {read} repositories read, {len(problems)} problem(s)")
    if read == 0:
        return 2
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
