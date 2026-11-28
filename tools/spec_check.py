"""Check the specification's traceability: input, brief, requirements, design, test scenarios, contracts.

Requirement files are read from every repository (DESIGN-4): the workspace's spec/requirements and each
child repository's folder named in tools/requirement_files.py, from clones next to this one.

Rules (spec/README.md, spec/requirements/README.md, R-WS-003, DESIGN-8):
- A requirement is a heading "### R-AREA-nnn Title". Its ID is unique across all files.
- It has a "Why:" line. Until every repository has moved to it, a missing Why line is counted and
  reported, and fails only in the workspace's own requirement files.
- It has a "Source:" line naming at least one existing ID: a question (Q-WS-) in spec/author-input/ or
  OPEN-QUESTIONS.md, a brief item (GOAL-, SCOPE-, PRINCIPLE-, CONSTRAINT-, ASSUMPTION-, RISK-, DEPENDENCY-)
  in spec/brief.md, a design choice (DESIGN-) in spec/design/system.md, a PCM decision (D-) in the
  private-cloud-manager clone, or, while DECISIONS.md exists, a workspace decision (WD-).
- It has at least one test scenario: a line "- T-AREA-nnnx (anywhere|lab, ...)" whose number is
  the requirement's. A dropped requirement ("### R-AREA-nnn Dropped: ...") keeps its ID and Source and
  has no scenario.
- Every scenario belongs to an existing requirement.
- Every brief item and design choice ("- **PREFIX-n Title.**") has a unique ID and its lines (FIELDS): a "Why:",
  or an assumption's "Status:", a risk's "Effect:", "Reduced by:" and "Acts:", a dependency's "Provided by:" and
  "Needed by:"; a design choice also has "Rejected:" and "Serves:". Every ID either names exists.
- Every contract row in spec/design/system.md, section Contracts, names a check file in checks/ that
  exists and that checks/run_all.py runs, or says it is planned in a ROADMAP milestone (R-WS-001).

    python tools/spec_check.py                    # every repository; exit 1 on any problem
    python tools/spec_check.py --repos agent-e2   # only these child repositories (CI cannot read isvara)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from requirement_files import WORKSPACE, add_repos_argument, files

ROOT = Path(__file__).resolve().parents[1]
PCM_DECISIONS = ROOT.parent / "private-cloud-manager" / "decisions.md"

REQ = re.compile(r"^### (R-[A-Z0-9]+-\d{3})\b( Dropped:)?", re.M)
SCEN = re.compile(r"^- (T-[A-Z0-9]+-\d{3}[a-z]) \(([a-z]+)", re.M)
SOURCE = re.compile(r"^Source:(.*)$", re.M)
ITEM_PREFIXES = "GOAL|SCOPE|PRINCIPLE|CONSTRAINT|ASSUMPTION|RISK|DEPENDENCY|DESIGN"
CITED = re.compile(rf"\b(Q-WS-I?\d+|WD-\d{{3}}|D-\d{{3}}|(?:{ITEM_PREFIXES})-\d+)\b")
WHY = re.compile(r"^Why:\s*\S", re.M)
BRIEF = ROOT / "spec" / "brief.md"
DESIGN = ROOT / "spec" / "design" / "system.md"
ITEM = re.compile(rf"^- \*\*((?:{ITEM_PREFIXES})-\d+) ", re.M)
ANY_ID = re.compile(rf"\b(Q-WS-I?\d+|WD-\d{{3}}|(?:{ITEM_PREFIXES})-\d+|R-[A-Z0-9]+-\d{{3}}|C\d)\b")


def items(path: Path) -> dict[str, str]:
    """Brief items or design choices: ID -> the text of its bullet block."""
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    heads = list(ITEM.finditer(text))
    out: dict[str, str] = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = re.split(r"\n(?=#|- \*\*|\n[^ -])", text[m.start(): end], maxsplit=1)[0]
        key = m.group(1) if m.group(1) not in out else m.group(1) + "#dup"
        out[key] = block
    return out


def known_ids() -> set[str]:
    ids: set[str] = set()
    for f in list((ROOT / "spec" / "author-input").glob("*.md")) + [ROOT / "OPEN-QUESTIONS.md"]:
        if f.exists():
            ids |= set(re.findall(r"^#{2,4} (Q-WS-I?\d+)\b", f.read_text(encoding="utf-8"), re.M))
    decisions = ROOT / "DECISIONS.md"
    if decisions.exists():
        ids |= set(re.findall(r"^## (WD-\d{3}) ", decisions.read_text(encoding="utf-8"), re.M))
    ids |= {k for k in items(BRIEF) | items(DESIGN) if "#" not in k}
    if PCM_DECISIONS.exists():
        ids |= set(re.findall(r"^## (D-\d{3}) ", PCM_DECISIONS.read_text(encoding="utf-8"), re.M))  # one block per decision (D-134)
    return ids


# The lines each kind of item must have; every other kind needs a Why.
FIELDS = {
    "ASSUMPTION": ["Status:"],
    "RISK": ["Effect:", "Reduced by:", "Acts:"],
    "DEPENDENCY": ["Provided by:", "Needed by:"],
    "DESIGN": ["Why:", "Rejected:", "Serves:"],
}


def item_problems(ids: set[str], reqs: dict[str, str], read_all: bool) -> list[str]:
    """Brief items and design choices: unique, with a reason, and naming only IDs that exist."""
    problems = []
    known = ids | set(reqs) | {f"C{n}" for n in range(1, 6)}
    for path in (BRIEF, DESIGN):
        name = path.relative_to(ROOT).as_posix()
        if not path.exists():
            problems.append(f"{name}: missing")
            continue
        for iid, block in items(path).items():
            if "#dup" in iid:
                problems.append(f"{name}: {iid[:-4]} is used twice")
                continue
            fields = FIELDS.get(iid.split("-")[0], ["Why:"])
            for field in fields:
                if field not in block:
                    problems.append(f"{name}: {iid} has no {field}")
            for ref in set(ANY_ID.findall(block)):
                if ref.startswith("R-") and not read_all:
                    continue  # a requirement of a repository CI cannot read
                if ref not in known:
                    problems.append(f"{name}: {iid} names {ref}, which does not exist")
    return problems


CONTRACT_ROW = re.compile(r"^\| (C\d+) \|(.*)$", re.M)
CHECK_LINK = re.compile(r"\]\((?:\.\./\.\./)?(checks/[\w./-]+\.py)\)")
PLANNED = re.compile(r"planned in ROADMAP M\d+", re.I)


def contract_problems() -> list[str]:
    """Each contract row names a running check that exists and run_all.py runs, or a milestone that plans one."""
    problems = []
    run_all = (ROOT / "checks" / "run_all.py").read_text(encoding="utf-8")
    text = DESIGN.read_text(encoding="utf-8")
    rows = CONTRACT_ROW.findall(text[text.find("## Contracts"):])
    if not rows:
        problems.append("spec/design/system.md: no contract rows found in section Contracts")
    for cid, rest in rows:
        check = rest.rstrip(" |").rsplit("|", 1)[-1]
        link = CHECK_LINK.search(check)
        if link:
            path = ROOT / link.group(1)
            if not path.is_file():
                problems.append(f"spec/design/system.md: {cid} names {link.group(1)}, which does not exist")
            elif f'"{path.name}"' not in run_all:
                problems.append(f"spec/design/system.md: {cid} names {link.group(1)}, which checks/run_all.py does not run")
        elif not PLANNED.search(check):
            problems.append(f"spec/design/system.md: {cid} names no check and no milestone that plans one")
    return problems


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
    no_why: dict[str, int] = {}
    scenarios: list[tuple[str, str, str]] = []
    for f in req_files:
        text = f.path.read_text(encoding="utf-8")
        heads = list(REQ.finditer(text))
        for i, m in enumerate(heads):
            rid = m.group(1)
            body = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
            body = body.split("\n## ", 1)[0]
            if rid in reqs:
                problems.append(f"{f.name}: {rid} is also in {reqs[rid]}")
            reqs[rid] = f.name
            if not m.group(2) and not WHY.search(body):
                if f.repo == WORKSPACE:
                    problems.append(f"{f.name}: {rid} has no Why line")
                else:
                    no_why[f.repo] = no_why.get(f.repo, 0) + 1
            src = SOURCE.search(body)
            if not src:
                problems.append(f"{f.name}: {rid} has no Source line")
            else:
                cited = CITED.findall(src.group(1))
                if not cited:
                    problems.append(f"{f.name}: {rid} Source names no question, brief item, design choice or decision ID")
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
    problems += item_problems(ids, reqs, read_all=not unread)
    problems += contract_problems()
    for p in problems:
        print(f"FAIL {p}")
    for repo, n in sorted(no_why.items()):
        print(f"TO MOVE {repo}: {n} requirement(s) have no Why line yet")
    for repo in unread:
        print(f"NOT RUN {repo}: its requirements were not read")
    lab = sum(1 for _, w, _ in scenarios if w == "lab")
    print(f"spec: {len(reqs)} requirements, {len(scenarios)} test scenarios ({lab} lab), {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
