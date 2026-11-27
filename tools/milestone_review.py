"""Write one review page per milestone: every requirement the author approves, on one page.

The requirement files hold the full text for the agent. The author approves a milestone from one page:
each requirement as a single line, grouped by requirement file, with a link to its full text and the
number of its test scenarios that run anywhere and in the lab.

A milestone's requirements are the IDs its section in ROADMAP.md names (single IDs and ranges such as
"R-KPI-001 to R-KPI-006"), plus every requirement whose "Milestone:" line names it. Dropped
requirements are listed apart, for reference.

Each requirement that is not dropped belongs to exactly one milestone, or its "Milestone:" line says
"after release 1.0" (WD-042). A requirement with a test scenario that needs the lab belongs to a milestone
whose section says "**Runs:** in the lab", or to after release 1.0 (WD-042). Both modes fail otherwise.

Requirement files are read from every repository (WD-036, tools/requirement_files.py). A page that lists a
requirement of a repository not read (CI cannot read isvara) is reported as not run, never as checked.

    python tools/milestone_review.py           # write spec/review/M<n>.md for each milestone with requirements
    python tools/milestone_review.py --check   # exit 1 when a page differs from what the files say
    python tools/milestone_review.py --check --repos agent-e2 PCM-Adapter private-cloud-manager   # CI
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from requirement_files import OWNER, ReqFile, add_repos_argument, files

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "spec" / "review"

MILESTONE = re.compile(r"^### (M\d+) (.+)$", re.M)
ID = r"R-[A-Z0-9]+-\d{3}"
RANGE = re.compile(rf"({ID}) to ({ID})")
SINGLE = re.compile(rf"\b({ID})\b")
REQ = re.compile(rf"^### ({ID}) (.+)$", re.M)
SCEN = re.compile(r"^- T-[A-Z0-9]+-\d{3}[a-z] \(([a-z]+)", re.M)
MILESTONE_LINE = re.compile(r"^Milestone: (.+)$", re.M)


def slug(heading: str) -> str:
    """The anchor GitHub gives a heading."""
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def expand(text: str) -> list[str]:
    """Every requirement ID a piece of ROADMAP text names, ranges expanded."""
    ids: list[str] = []
    for a, b in RANGE.findall(text):
        prefix, first, last = a.rsplit("-", 1)[0], int(a[-3:]), int(b[-3:])
        if b.rsplit("-", 1)[0] == prefix:
            ids += [f"{prefix}-{n:03d}" for n in range(first, last + 1)]
    ids += SINGLE.findall(RANGE.sub("", text))
    return ids


def requirements(req_files: list[ReqFile]) -> dict[str, dict]:
    reqs: dict[str, dict] = {}
    for rf in req_files:
        f = rf.path
        text = f.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, re.M)
        area = h1.group(1) if h1 else f.stem
        area = re.sub(r"^Requirements: ", "", area)
        area = re.sub(r" requirements$", "", area)
        area = area[:1].upper() + area[1:]
        heads = list(REQ.finditer(text))
        for i, m in enumerate(heads):
            body = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
            body = body.split("\n## ", 1)[0]
            rid, title = m.group(1), m.group(2).strip()
            where = SCEN.findall(body)
            ms = MILESTONE_LINE.search(body)
            reqs[rid] = {
                "file": f.name, "link": rf.link(), "area": area, "title": title, "anchor": slug(f"{rid} {title}"),
                "dropped": title.startswith("Dropped:"),
                "anywhere": where.count("anywhere"), "lab": where.count("lab"),
                "milestones": set(re.findall(r"\bM\d+\b", ms.group(1))) if ms else set(),
                "after": bool(ms and re.search(r"after release 1\.0", ms.group(1), re.I)),
            }
    return reqs


def milestones(reqs: dict[str, dict]) -> dict[str, tuple[str, list[str]]]:
    text = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    heads = list(MILESTONE.finditer(text))
    out: dict[str, tuple[str, list[str]]] = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        section = text[m.end(): end].split("\n## ", 1)[0]
        ids = [r for r in expand(section) if r in reqs]
        ids += [r for r, v in reqs.items() if m.group(1) in v["milestones"]]
        seen: list[str] = []
        for r in ids:
            if r not in seen:
                seen.append(r)
        if seen:
            out[m.group(1)] = (m.group(2).strip(), seen)
    return out


def lab_milestones() -> set[str]:
    """The milestones whose section in ROADMAP.md says they run in the lab."""
    text = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    heads = list(MILESTONE.finditer(text))
    out = set()
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        if "**Runs:** in the lab" in text[m.end(): end].split("\n## ", 1)[0]:
            out.add(m.group(1))
    return out


def membership(reqs: dict[str, dict], ms: dict[str, tuple[str, list[str]]]) -> list[str]:
    """Each requirement in exactly one milestone, or after release 1.0; lab tests only in a lab milestone (WD-042)."""
    lab = lab_milestones()
    where: dict[str, list[str]] = {}
    for mid, (_, ids) in ms.items():
        for r in ids:
            where.setdefault(r, []).append(mid)
    problems = []
    for r, v in reqs.items():
        if v["dropped"]:
            continue
        found = where.get(r, [])
        if len(found) > 1:
            problems.append(f"{r} belongs to {' and '.join(found)}: one milestone per requirement")
        elif not found and not v["after"]:
            problems.append(f"{r} belongs to no milestone: name it in ROADMAP.md or give it a Milestone line")
        elif found and v["after"]:
            problems.append(f"{r} is after release 1.0 and also in {found[0]}")
        if v["lab"] and len(found) == 1 and found[0] not in lab:
            problems.append(f"{r} has a lab test scenario but {found[0]} does not run in the lab: move the scenario")
    return problems


def page(mid: str, title: str, ids: list[str], reqs: dict[str, dict]) -> str:
    live = [r for r in ids if not reqs[r]["dropped"]]
    dropped = [r for r in ids if reqs[r]["dropped"]]
    lines = [
        f"# {mid} review",
        "",
        f"Milestone {mid}: {title}.",
        "",
        f"Every requirement of milestone {mid} on one page, for the author's approval. Each line is one requirement: its ID, what it says, and how many of its test scenarios run anywhere and how many need the lab. The ID links to the full text. This page is generated by [tools/milestone_review.py](../../tools/milestone_review.py) from the requirement files and [ROADMAP.md](../../ROADMAP.md); edit those, never this page.",
        "",
        f"To approve: write \"Approved\" and the date under milestone {mid} in [ROADMAP.md](../../ROADMAP.md), or tell the agent. To reject a requirement, name its ID and the reason.",
        "",
        f"Requirements to approve: {len(live)}.",
    ]
    areas: dict[str, list[str]] = {}
    for r in live:
        areas.setdefault(reqs[r]["area"], []).append(r)
    for area, rs in areas.items():
        lines += ["", f"## {area}", ""]
        for r in rs:
            v = reqs[r]
            tests = f"{v['anywhere']} anywhere, {v['lab']} lab"
            lines.append(f"- [{r}]({v['link']}#{v['anchor']}) {v['title']}. Tests: {tests}.")
    if dropped:
        lines += ["", "## Dropped requirements", "", "Listed for reference; nothing to approve.", ""]
        for r in dropped:
            v = reqs[r]
            lines.append(f"- [{r}]({v['link']}#{v['anchor']}) {cap(v['title'].removeprefix('Dropped: '))}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail when a page differs from the files")
    add_repos_argument(ap)
    args = ap.parse_args()
    req_files, unread, missing = files(args.repos)
    for repo in missing:
        print(f"COULD NOT RUN {repo}: no clone next to this repository")
    if missing:
        return 2
    if unread and not args.check:
        print(f"refusing to write pages without {', '.join(unread)}: they would lose its requirements")
        return 2
    reqs = requirements(req_files)
    unread_links = tuple(f"github.com/{OWNER}/{r}/" for r in unread)
    pages = {f"{mid}.md": page(mid, t, ids, reqs) for mid, (t, ids) in milestones(reqs).items()}
    problems = membership(reqs, milestones(reqs))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    not_run = []
    for old in OUT_DIR.glob("*.md"):
        if any(u in old.read_text(encoding="utf-8") for u in unread_links):
            not_run.append(old.name)
    for name, content in pages.items():
        path = OUT_DIR / name
        if name in not_run:
            continue
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                problems.append(f"spec/review/{name} is out of date: run python tools/milestone_review.py")
        else:
            path.write_text(content, encoding="utf-8")
    for old in OUT_DIR.glob("*.md"):
        if old.name not in pages and old.name not in not_run:
            if args.check:
                problems.append(f"spec/review/{old.name} belongs to no milestone with requirements")
            else:
                old.unlink()
    for p in problems:
        print(f"FAIL {p}")
    for name in not_run:
        print(f"NOT RUN spec/review/{name}: it lists requirements of {', '.join(unread)}, which were not read")
    print(f"review: {len(pages)} milestone pages, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
