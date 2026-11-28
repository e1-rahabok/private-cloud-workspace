# /// script
# requires-python = ">=3.10"
# ///
"""Check of R-WS-007: no folder or file name carries a version, milestone or status word (DESIGN-6).

For each repository it reads the tracked paths (git ls-files) of its clone and fails on a folder or file name that
holds, as a whole word between separators (start or end, '-', '_', ' ', '.'), a version (v2, v5), a milestone (m5)
or a status word (proto, new, old, final, copy). A file's extension is not part of its name. Words inside a longer
word do not count: `thresholds-performance.yaml` holds no "old".

Outside the check, by R-WS-007: names that are titles written for readers or for the model, which describe their
content (EXEMPT below), and the review pages spec/review/M<n>.md, each named for the milestone it reviews.

A repository with no clone is reported as not run: isvara is private, so the workspace's CI cannot read it, and
isvara's own CI runs this check (R-WS-002). checks/test_file_names.py plants a break and expects a failure.
Exit 0: no problem. Exit 1: a problem. Exit 2: no repository could be read.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPOS = ["private-cloud-workspace", "agent-e2", "PCM-Adapter", "private-cloud-manager", "isvara"]
WORD = re.compile(r"(?:^|[-_ .])(v\d+|m\d+|proto|new|old|final|copy)(?=$|[-_ .])", re.IGNORECASE)
# Folders whose names are titles for readers or for the model (R-WS-007), and review pages named for a milestone.
EXEMPT = {
    "agent-e2": ["knowledge/", "benchmark/questions/"],
    "PCM-Adapter": ["Management Pack/content/"],
}
REVIEW_PAGE = re.compile(r"^spec/review/M\d+\.md$")


def tracked(clone: Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(clone), "ls-files"], capture_output=True, text=True, check=True).stdout
    return [line for line in out.split("\n") if line]


def problems_in(repo: str, paths: list[str]) -> list[str]:
    """Each flagged folder or file name, once, as repo: path (word)."""
    found: dict[str, str] = {}
    for path in paths:
        if any(path.startswith(e) for e in EXEMPT.get(repo, [])) or REVIEW_PAGE.match(path):
            continue
        parts = path.split("/")
        for i, part in enumerate(parts):
            name = part
            if i == len(parts) - 1 and "." in part[1:]:
                name = part.rsplit(".", 1)[0]  # a file's extension is not part of its name
            m = WORD.search(name)
            if m:
                found.setdefault("/".join(parts[: i + 1]), m.group(1))
    return [f"{repo}: '{p}' holds '{w}'" for p, w in sorted(found.items())]


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
        problems += problems_in(repo, tracked(clone))
    for repo in not_run:
        print(f"NOT RUN {repo}: no clone")
    for p in problems:
        print(f"FAIL {p}")
    print(f"R-WS-007 file names: {read} repositories read, {len(problems)} problem(s)")
    if read == 0:
        return 2
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
