"""Check the specification's links: requirements, test scenarios and their sources.

Requirement files are read from every repository (WD-036): the workspace's spec/requirements and each
child repository's folder named in tools/requirement_files.py, from clones next to this one.

Rules (spec/requirements/README.md and requirement R-WS-003):
- A requirement is a heading "### R-AREA-nnn Title". Its ID is unique across all files.
- It has a "Source:" line naming at least one existing question (Q-WS-), workspace decision (WD-) or
  PCM decision (D-). Questions are found in spec/interview-round-*.md and OPEN-QUESTIONS.md,
  workspace decisions in DECISIONS.md, PCM decisions in the private-cloud-manager clone.
- It has at least one test scenario: a line "- T-AREA-nnnx (anywhere|lab, ...)" whose number is
  the requirement's. A dropped requirement ("### R-AREA-nnn Dropped: ...") keeps its ID and Source and
  has no scenario (spec/requirements/README.md, Rules).
- Every scenario belongs to an existing requirement.

    python tools/spec_check.py                    # every repository; exit 1 on any problem
    python tools/spec_check.py --repos agent-e2   # only these child repositories (CI cannot read isvara)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from requirement_files import add_repos_argument, files

ROOT = Path(__file__).resolve().parents[1]
PCM_DECISIONS = ROOT.parent / "private-cloud-manager" / "decisions.md"

REQ = re.compile(r"^### (R-[A-Z0-9]+-\d{3})\b( Dropped:)?", re.M)
SCEN = re.compile(r"^- (T-[A-Z0-9]+-\d{3}[a-z]) \(([a-z]+)", re.M)
SOURCE = re.compile(r"^Source:(.*)$", re.M)
CITED = re.compile(r"\b(Q-WS-I?\d+|WD-\d{3}|D-\d{3})\b")


def known_ids() -> set[str]:
    ids: set[str] = set()
    for f in list((ROOT / "spec").glob("interview-round-*.md")) + [ROOT / "OPEN-QUESTIONS.md"]:
        if f.exists():
            ids |= set(re.findall(r"^#{2,4} (Q-WS-I?\d+)\b", f.read_text(encoding="utf-8"), re.M))
    ids |= set(re.findall(r"^## (WD-\d{3}) ", (ROOT / "DECISIONS.md").read_text(encoding="utf-8"), re.M))
    if PCM_DECISIONS.exists():
        ids |= set(re.findall(r"^\| (D-\d{3}) \|", PCM_DECISIONS.read_text(encoding="utf-8"), re.M))
    return ids


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    add_repos_argument(ap)
    args = ap.parse_args()
    req_files, unread, missing = files(args.repos)
    for repo in missing:
        print(f"COULD NOT RUN {repo}: no clone next to this repository")
    if missing:
        return 2
    ids = known_ids()
    problems: list[str] = []
    reqs: dict[str, str] = {}
    scenarios: list[tuple[str, str, str]] = []
    for rf in req_files:
        f = rf
        text = rf.path.read_text(encoding="utf-8")
        heads = list(REQ.finditer(text))
        for i, m in enumerate(heads):
            rid = m.group(1)
            body = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
            body = body.split("\n## ", 1)[0]
            if rid in reqs:
                problems.append(f"{f.name}: {rid} is also in {reqs[rid]}")
            reqs[rid] = f.name
            src = SOURCE.search(body)
            if not src:
                problems.append(f"{f.name}: {rid} has no Source line")
            else:
                cited = CITED.findall(src.group(1))
                if not cited:
                    problems.append(f"{f.name}: {rid} Source names no question or decision ID")
                for c in cited:
                    if c not in ids:
                        problems.append(f"{f.name}: {rid} Source names {c}, which does not exist")
            own = [s for s in SCEN.finditer(body) if "R-" + s.group(1)[2:-1] == rid]
            if not own and not m.group(2):
                problems.append(f"{f.name}: {rid} has no test scenario")
        for s in SCEN.finditer(text):
            scenarios.append((s.group(1), s.group(2), f.name))
    for sid, where, fname in scenarios:
        rid = "R-" + sid[2:-1]
        if rid not in reqs:
            problems.append(f"{fname}: {sid} belongs to no requirement ({rid})")
        if where not in ("anywhere", "lab"):
            problems.append(f"{fname}: {sid} says it runs '{where}'; use anywhere or lab")
    for p in problems:
        print(f"FAIL {p}")
    for repo in unread:
        print(f"NOT RUN {repo}: its requirements were not read")
    lab = sum(1 for _, w, _ in scenarios if w == "lab")
    print(f"spec: {len(reqs)} requirements, {len(scenarios)} test scenarios ({lab} lab), {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
