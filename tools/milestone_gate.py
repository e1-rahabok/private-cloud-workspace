"""The milestone gate: work happens only in the earliest milestone of ROADMAP.md that is not done (DESIGN-21).

ROADMAP.md format the gate reads:
- A milestone is a heading `### M<n> <title>`. The numbers run M1, M2, M3 in file order, with no gap and no
  M0 (DESIGN-21). It is done when the heading ends with `: done`. Claude writes `: done` only after the author
  has approved the milestone.
- No file or folder is owned by two milestones (DESIGN-21).
- The open milestone is the first one, in file order, that is not done.
- Its next item is the first `- [ ]` line in its section.
- A `- Files in this repository:` line lists the files the milestone owns, in backticks. A path that ends
  with `/` is a folder and owns everything under it. A file listed under no milestone is owned by none.

    python tools/milestone_gate.py                  # print the open milestone and its next item
    python tools/milestone_gate.py --hook           # the same, worded for Claude; run on every prompt
    python tools/milestone_gate.py --check BASE     # exit 1 if the change from BASE to HEAD touches a
                                                    # file owned only by milestones after the open one,
                                                    # or if the numbering or the ownership is broken
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r"^### (M-?\d+) (.+?)\s*$", re.M)
FILES = re.compile(r"^- Files in this repository: (.+)$", re.M)
ITEM = re.compile(r"^- \[ \] (.+)$", re.M)


def milestones() -> list[dict]:
    text = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    heads = list(HEADING.finditer(text))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        section = text[m.end(): end].split("\n## ", 1)[0]
        title = m.group(2)
        files = [p for line in FILES.findall(section) for p in re.findall(r"`([^`]+)`", line)]
        items = ITEM.findall(section)
        out.append({"id": m.group(1), "title": title, "done": title.endswith(": done"),
                    "files": files, "next": items[0] if items else None})
    return out


def owns(path: str, pattern: str) -> bool:
    return path.startswith(pattern) if pattern.endswith("/") else path == pattern


def structure(ms: list[dict]) -> list[str]:
    """Problems with the milestones themselves: numbering and files owned twice (DESIGN-21)."""
    problems = []
    for n, m in enumerate(ms, 1):
        if m["id"] != f"M{n}":
            problems.append(f"milestone {n} in ROADMAP.md is {m['id']}: number them M1, M2, M3 in order")
    for i, a in enumerate(ms):
        for b in ms[i + 1:]:
            for p in a["files"]:
                for q in b["files"]:
                    if owns(p, q) or owns(q, p):
                        problems.append(f"{a['id']} owns {p} and {b['id']} owns {q}: one milestone per file")
    return problems


def open_milestone(ms: list[dict]) -> int | None:
    return next((i for i, m in enumerate(ms) if not m["done"]), None)


def status(hook: bool) -> int:
    ms = milestones()
    i = open_milestone(ms)
    if i is None:
        print("Milestone gate: every milestone in ROADMAP.md is done.")
        return 0
    m = ms[i]
    nxt = m["next"] or "no open item; ask the author to approve the milestone"
    for p in structure(ms):
        print(f"Milestone gate: FAIL {p}")
    if hook:
        print(f"Milestone gate (DESIGN-21): the open milestone is {m['id']} {m['title']}.")
        print(f"Its next item: {nxt}")
        print(f"Work only on {m['id']}. Park any request for a later milestone in one line and act on nothing in it.")
    else:
        print(f"{m['id']} {m['title']}\nNext item: {nxt}")
    return 0


def check(base: str) -> int:
    ms = milestones()
    i = open_milestone(ms)
    if i is None:
        return 0
    allowed = [p for m in ms[: i + 1] for p in m["files"]]
    later = [(m["id"], p) for m in ms[i + 1:] for p in m["files"]]
    # Committed, staged, unstaged and untracked changes since the branch left BASE, so the check
    # also works before a commit.
    mb = subprocess.run(["git", "merge-base", base, "HEAD"], cwd=ROOT, capture_output=True, text=True)
    if mb.returncode:
        print(f"could not find where HEAD left {base}: {mb.stderr.strip()}")
        return 2
    changed = subprocess.run(["git", "diff", "--name-only", mb.stdout.strip()], cwd=ROOT,
                             capture_output=True, text=True).stdout.split()
    changed += subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT,
                              capture_output=True, text=True).stdout.split()
    problems = 0
    for p in structure(ms):
        problems += 1
        print(f"FAIL {p}")
    for path in sorted(set(changed)):
        if any(owns(path, p) for p in allowed):
            continue
        owners = sorted({mid for mid, p in later if owns(path, p)})
        if owners:
            problems += 1
            print(f"FAIL {path}: owned by {', '.join(owners)}; the open milestone is {ms[i]['id']}")
    print(f"gate: open milestone {ms[i]['id']}, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--check"] and len(args) == 2:
        sys.exit(check(args[1]))
    sys.exit(status(hook=args == ["--hook"]))
