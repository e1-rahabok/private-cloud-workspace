"""Every repository holds the same CLAUDE.md as this workspace, and its own CLAUDE-PROJECT.md (DESIGN-22).

CLAUDE.md is the method, for any project; CLAUDE-PROJECT.md is the repository's own rules. The clones sit
next to this repository, as for checks/run_all.py.

    python tools/claude_md_copies.py                         # the four child repositories
    python tools/claude_md_copies.py agent-e2 PCM-Adapter    # only these (CI cannot read isvara)

Exit 0 when every copy is equal, 1 when one differs or a file is missing, 2 when a clone is missing.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOS = ["agent-e2", "PCM-Adapter", "private-cloud-manager", "isvara"]


def main(names: list[str]) -> int:
    method = (ROOT / "CLAUDE.md").read_bytes()
    problems = missing = 0
    for name in names or REPOS:
        repo = ROOT.parent / name
        if not repo.is_dir():
            print(f"NOT RUN {name}: no clone at {repo}")
            missing += 1
            continue
        copy = repo / "CLAUDE.md"
        if not copy.is_file():
            print(f"FAIL {name}: no CLAUDE.md")
            problems += 1
        elif copy.read_bytes() != method:
            print(f"FAIL {name}: CLAUDE.md differs from the workspace's; copy the workspace's file")
            problems += 1
        if not (repo / "CLAUDE-PROJECT.md").is_file():
            print(f"FAIL {name}: no CLAUDE-PROJECT.md")
            problems += 1
    print(f"claude_md: {len(names or REPOS) - missing} repositories checked, {problems} problem(s)")
    return 1 if problems else 2 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
