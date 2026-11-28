"""Write one review page per milestone, in plain words, for the author's approval.

R-WS-015 (DESIGN-30). The author is the expert in private cloud operations and is not a software developer, so a
page says what the milestone set out to do and why, what changes, what the author is asked to do, what the author
confirms, what Claude built and owns, what was left out, what could go wrong, and in one line how it was tested.
It carries no test count, no ID and no file name. It is built from three sources and states no fact of its own:

- the milestone's section in ROADMAP.md: the fields "In plain words", "What changes", "Left out on purpose" and
  "The author", and the work lines, ticked or not;
- each requirement's title, Why and Source: a requirement whose Source records an answer of the author or the
  author's words is listed under what the author confirms, with the words quoted; one that rests only on a design
  choice is listed under what Claude built, for information;
- the brief: the goals, scope, principles, constraints, assumptions and risks that the requirements and the
  roadmap section name.

A milestone's requirements are the IDs its section in ROADMAP.md names (single IDs and ranges such as
"R-KPI-001 to R-KPI-006"), plus every requirement whose "Milestone:" line names it. Dropped requirements are
listed apart, as left out.

Each requirement that is not dropped belongs to exactly one milestone, or its "Milestone:" line says
"after release 1.0" (DESIGN-21). A requirement with a test scenario that needs the lab belongs to a milestone
whose section says "**Runs:** in the lab", or to after release 1.0 (DESIGN-21). Both modes fail otherwise.

The open milestone, the first whose heading does not end with ": done", must have all four fields. The tool removes
every ID citation from the text it copies and fails when an ID, a file name or a test count remains in a page.

Requirement files are read from every repository (DESIGN-4, tools/requirement_files.py). A page that lists a
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
WHY_LINE = re.compile(r"^Why: (.+)$", re.M)
SOURCE_LINE = re.compile(r"^Source: (.+)$", re.M)

# Every kind of ID a page must not carry: requirements, tests, questions, decisions, design choices and brief items.
BRIEF_KINDS = ("GOAL", "SCOPE", "PRINCIPLE", "CONSTRAINT", "ASSUMPTION", "RISK")
BRIEF_ID = re.compile(rf"\b((?:{'|'.join(BRIEF_KINDS)})-\d+)\b")
ID_TOKEN = re.compile(
    r"\b(?:(?:R|T)-[A-Z0-9]+-\d{3}[a-z]?|Q-[A-Z0-9]+-[A-Z]?\d+|D-\d{3}|"
    r"(?:DESIGN|GOAL|SCOPE|PRINCIPLE|CONSTRAINT|ASSUMPTION|RISK|DEPENDENCY)-\d+)\b")
FILE_NAME = re.compile(r"\b[\w-]+(?:\.[\w-]+)*\.(?:md|py|ya?ml|json|ps1|mjs|tsx?|sh|txt)\b")
TEST_COUNT = re.compile(r"\bTests:|\b\d+ (?:anywhere|lab)\b")
ANSWER_OF_THE_AUTHOR = re.compile(r"\bQ-[A-Z0-9]+-[A-Z]?\d+|\bthe author\b|\bauthor's\b", re.I)
QUOTE = re.compile(r"[\"“]([^\"”]{15,}?)[\"”]")

# The sections of a page, in order (R-WS-015). The open milestone's page needs every one of them filled.
SECTIONS = [
    "Purpose and reason",
    "Changes for users and for you",
    "Input needed from you",
    "Facts you confirm",
    "Work I built and own",
    "Scope left out on purpose",
    "Risks",
    "Testing",
]
FIELDS = {"In plain words": "plain", "What changes": "changes", "Left out on purpose": "left", "What I need from you": "need"}
OPTIONAL_FIELDS = {"Risks": "risks", "The author": "author"}
LATER = "I write this when the milestone opens."
KIND = {"GOAL": "Goal", "SCOPE": "Scope", "PRINCIPLE": "Principle", "CONSTRAINT": "Constraint", "ASSUMPTION": "Assumption"}
REFERENCE = re.compile(r"^(?:see |the )?(?:brief|system design|test plan|glossary|round \d+|[\w ]+ in the (?:brief|system design))\b", re.I)


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
            why, source = WHY_LINE.search(body), SOURCE_LINE.search(body)
            reqs[rid] = {
                "file": f.name, "link": rf.link(), "area": area, "title": title, "anchor": slug(f"{rid} {title}"),
                "dropped": title.startswith("Dropped:"),
                "why": why.group(1).strip() if why else "", "source": source.group(1).strip() if source else "",
                "anywhere": where.count("anywhere"), "lab": where.count("lab"),
                "milestones": set(re.findall(r"\bM\d+\b", ms.group(1))) if ms else set(),
                "after": bool(ms and re.search(r"after release 1\.0", ms.group(1), re.I)),
            }
    return reqs


def roadmap_sections(text: str) -> dict[str, dict]:
    """Each milestone's title, state, fields, work lines and body, from ROADMAP.md."""
    heads = list(MILESTONE.finditer(text))
    out: dict[str, dict] = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[m.end(): end].split("\n## ", 1)[0]
        raw = m.group(2).strip()
        state = re.search(r": (done|in progress)$", raw)
        fields = {}
        for name, key in {**FIELDS, **OPTIONAL_FIELDS}.items():
            f = re.search(rf"^- \*\*{re.escape(name)}:\*\* (.+)$", body, re.M)
            if f:
                fields[key] = f.group(1).strip()
        work = re.findall(r"^- \[( |x)\] (.+)$", body, re.M)
        out[m.group(1)] = {
            "title": raw[: state.start()] if state else raw, "done": bool(state and state.group(1) == "done"),
            "fields": fields, "body": body,
            "open_work": [w for done, w in work if done == " " and not w.startswith("Approval:")],
        }
    return out


def open_milestone(sections: dict[str, dict]) -> str | None:
    for mid, s in sections.items():
        if not s["done"]:
            return mid
    return None


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
    """Each requirement in exactly one milestone, or after release 1.0; lab tests only in a lab milestone (DESIGN-21)."""
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


def brief_items(text: str) -> dict[str, dict]:
    """The goals, scope, principles, constraints, assumptions and risks of the brief, each with its sub-bullets."""
    items: dict[str, dict] = {}
    heading, current = "", None
    for line in text.splitlines():
        if line.startswith("## "):
            heading, current = line[3:].strip(), None
            continue
        m = re.match(rf"^- \*\*((?:{'|'.join(BRIEF_KINDS)})-\d+) (.+?)\*\*\s*(.*)$", line)
        if m:
            current = {"id": m.group(1), "title": m.group(2).strip().rstrip("."), "text": m.group(3).strip(),
                       "subs": [], "section": heading}
            items[m.group(1)] = current
        elif current is not None and re.match(r"^\s+- ", line):
            current["subs"].append(line.strip()[2:])
        elif line.strip() and not line.startswith(" "):
            current = None
    return items


def design_titles(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip().rstrip(".")
            for m in re.finditer(r"^- \*\*(DESIGN-\d+) (.+?)\*\*", text, re.M)}


def humanize(name: str) -> str:
    """A file name as words: visitor-experience.md becomes visitor experience."""
    return re.sub(r"[-_]+", " ", re.sub(r"\.[A-Za-z]+$", "", name)).lower()


def drop_id_parens(s: str) -> str:
    """Remove each parenthesis that holds only IDs, and the IDs inside a parenthesis that holds more."""
    def inner(m: re.Match) -> str:
        body = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", m.group(1))
        if REFERENCE.match(body.strip()):
            return ""
        if not ID_TOKEN.search(body):
            return m.group(0)
        rest = ID_TOKEN.sub("", body)
        if not re.sub(r"\b(?:and|to|in|round \d+)\b|[\s,;:.]", "", rest):
            return ""
        rest = re.sub(r"^[\s,;:]+|[\s,;:]+$", "", rest)
        return f" ({rest})"
    return re.sub(r"\s*\(([^()]*)\)", inner, s)


TITLES: dict[str, str] = {}


def plain(s: str) -> str:
    """Text as the author reads it: links become their words, ID citations and code marks go."""
    s = drop_id_parens(s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", lambda m: humanize(m.group(1)) if FILE_NAME.fullmatch(m.group(1)) else m.group(1), s)
    s = re.sub(r"\b((?:%s)-\d+)\b" % "|".join(BRIEF_KINDS + ("DESIGN",)),
               lambda m: f"\u201c{TITLES[m.group(1)]}\u201d" if m.group(1) in TITLES else m.group(0), s)
    s = FILE_NAME.sub(lambda m: humanize(m.group(0)), s)
    s = s.replace("`", "")
    s = re.sub(r"\bWhy: ", "Reason: ", s)
    s = re.sub(r"\s+([.,;:])", r"\1", s)
    return re.sub(r"\s{2,}", " ", s).strip()


def item_text(item: dict) -> str:
    """One brief item as sentences: the words before its Source, without its Source, Acts or Check."""
    parts = [item["text"]] + item["subs"]
    out = []
    for part in parts:
        part = re.sub(r"\s*\bSource:.*$", "", part)
        part = re.sub(r"\s*\bActs:.*$", "", part)
        part = part.strip()
        if part:
            out.append(plain(part))
    return " ".join(out)


def quotes(source: str) -> list[str]:
    return [q.strip() for q in QUOTE.findall(plain_keep_quotes(source))][:2]


def plain_keep_quotes(s: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)


def brief_ids_in(*texts: str) -> list[str]:
    seen: list[str] = []
    for t in texts:
        for i in BRIEF_ID.findall(t):
            if i not in seen:
                seen.append(i)
    return seen


def ensure_stop(s: str) -> str:
    s = s.strip()
    return s if s.endswith((".", "!", "?", ":")) else s + "."


def tested_line(section: dict, has_lab: bool, state: str) -> str:
    if state == "later":
        return "Nothing of this milestone is built yet, so nothing has been tested."
    if section["open_work"]:
        line = "The work of this milestone is not finished, so I have not asked for your approval and not every test has run."
    else:
        line = "I ran every test of this milestone, and all of them pass."
    if has_lab:
        line += " The tests that need your lab run in the lab session with you."
    return line


def status_line(section: dict, state: str, current: str | None) -> str:
    if state == "done":
        return "Approved."
    if state == "later":
        return f"Not started: this milestone opens after {current} is approved. This page shows what the plan says so far." if current else "Not started."
    if section["open_work"]:
        return "Not ready: some of this milestone's work is still open."
    return "Ready for your approval."


def page(mid: str, title: str, ids: list[str], reqs: dict[str, dict], section: dict, brief: dict[str, dict],
         state: str = "open", current: str | None = None) -> str:
    live = [r for r in ids if not reqs[r]["dropped"]]
    dropped = [r for r in ids if reqs[r]["dropped"]]
    f = {k: cap(v) for k, v in section["fields"].items()}
    mine = [r for r in live if ANSWER_OF_THE_AUTHOR.search(reqs[r]["source"])]
    owned = [r for r in live if r not in mine]
    cited = brief_ids_in(section["body"], section["fields"].get("risks", ""), *(reqs[r]["why"] + " " + reqs[r]["source"] for r in live))
    cited = [i for i in cited if i in brief]
    in_scope = [i for i in cited if brief[i]["id"].split("-")[0] in ("GOAL", "SCOPE", "PRINCIPLE", "CONSTRAINT", "ASSUMPTION")
                and brief[i]["section"] != "Out of release 1.0"]
    left_out = [i for i in cited if brief[i]["section"] == "Out of release 1.0"]
    risks = [i for i in cited if i.startswith("RISK-")]
    has_lab = any(reqs[r]["lab"] for r in live)
    clean_title = re.sub(r"\s*:\s*$", "", title)

    def block(rs: list[str]) -> list[str]:
        out: list[str] = []
        areas: dict[str, list[str]] = {}
        for r in rs:
            areas.setdefault(reqs[r]["area"], []).append(r)
        for area, group in areas.items():
            out += [f"### {area}", ""]
            for r in group:
                v = reqs[r]
                line = f"- **[{ensure_stop(cap(plain(v['title'])))}]({v['link']}#{v['anchor']})**"
                if v["why"]:
                    line += " " + ensure_stop(plain(cap(v["why"])))
                out.append(line)
                if r in mine:
                    for q in quotes(v["source"]):
                        out.append(f"  - You said: “{plain(q)}”")
            out.append("")
        return out

    lines = [f"# {mid} review: {clean_title}", "",
             status_line(section, state, current), "",
             f"## {SECTIONS[0]}", "", plain(f.get("plain", LATER)), "",
             f"## {SECTIONS[1]}", "", plain(f.get("changes", LATER)), "",
             f"## {SECTIONS[2]}", "", plain(f.get("need") or (("In the plan, the author " + section["fields"]["author"].strip()) if f.get("author") else LATER)), "",
             "To approve, tell me “approved”. To correct something, name the item and say what is wrong. I change the plan first, then rebuild what follows from it.", "",
             f"## {SECTIONS[3]}", "",
             "Each item below rests on what you told me; “the author” in an item is you. Say so when one is wrong or incomplete.", ""]
    lines += block(mine) or ["Nothing in this milestone rests on your input.", ""]
    if in_scope:
        lines += ["### The goals, scope, limits and assumptions behind them", ""]
        for i in in_scope:
            b = brief[i]
            lines.append(f"- **{KIND[i.split('-')[0]]}: {ensure_stop(plain(b['title']))}** {item_text(b)}".rstrip())
        lines.append("")
    lines += [f"## {SECTIONS[4]}", "",
              "These follow from my own design choices and ask nothing of you. Open one to read its full wording.", ""]
    lines += block(owned) or ["Nothing in this milestone rests only on my design choices.", ""]
    lines += [f"## {SECTIONS[5]}", "", plain(f.get("left", LATER)), ""]
    if left_out:
        lines += ["Also outside release 1.0:", ""]
        for i in left_out:
            b = brief[i]
            lines.append(f"- **{ensure_stop(plain(b['title']))}** {item_text(b)}".rstrip())
        lines.append("")
    if dropped:
        lines += ["Dropped from this milestone on purpose. The workspace keeps requirements only for agreements between repositories, and each of these is one repository\u2019s own matter:", ""]
        for r in dropped:
            v = reqs[r]
            lines.append(f"- {ensure_stop(cap(plain(v['title'].removeprefix('Dropped: '))))}")
        lines.append("")
    lines += [f"## {SECTIONS[6]}", ""]
    if risks:
        for i in risks:
            b = brief[i]
            lines.append(f"- **{ensure_stop(plain(b['title']))}** {item_text(b)}".rstrip())
        lines.append("")
    else:
        lines += ["No risk of the brief is tied to this milestone.", ""]
    lines += [f"## {SECTIONS[7]}", "", tested_line(section, has_lab, state), "",
              "This page is rebuilt from the plan every time the plan changes."]
    return "\n".join(lines) + "\n"


def page_problems(mid: str, text: str, section: dict, open_milestone_id: str | None) -> list[str]:
    """What is wrong with a page's text (R-WS-015): a count, an ID, a file name, or a missing section."""
    problems = []
    visible = re.sub(r"\]\([^)]*\)", "]", text)
    for pattern, what in ((TEST_COUNT, "a test count"), (ID_TOKEN, "an ID"), (FILE_NAME, "a file name")):
        for m in pattern.finditer(visible):
            problems.append(f"spec/review/{mid}.md carries {what}: “{m.group(0)}” (R-WS-015)")
    if mid == open_milestone_id:
        for name in FIELDS:
            if not section["fields"].get(FIELDS[name]):
                problems.append(f"ROADMAP.md: the open milestone {mid} has no “{name}” field (R-WS-015)")
        headings = re.findall(r"^## (.+)$", text, re.M)
        if headings != SECTIONS:
            problems.append(f"spec/review/{mid}.md has the sections {headings}, not {SECTIONS} (R-WS-015)")
    return problems


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
    ms = milestones(reqs)
    sections = roadmap_sections((ROOT / "ROADMAP.md").read_text(encoding="utf-8"))
    brief = brief_items((ROOT / "spec" / "brief.md").read_text(encoding="utf-8"))
    TITLES.clear()
    TITLES.update(design_titles((ROOT / "spec" / "design" / "system.md").read_text(encoding="utf-8")))
    TITLES.update({i: b["title"] for i, b in brief.items()})
    current = open_milestone(sections)
    unread_links = tuple(f"github.com/{OWNER}/{r}/" for r in unread)
    def state_of(mid: str) -> str:
        return "done" if sections[mid]["done"] else "open" if mid == current else "later"

    pages = {f"{mid}.md": page(mid, sections[mid]["title"] if mid in sections else t, ids, reqs, sections[mid], brief,
                               state_of(mid), current)
             for mid, (t, ids) in ms.items()}
    problems = membership(reqs, ms)
    for name, content in pages.items():
        mid = name[:-3]
        problems += page_problems(mid, content, sections[mid], current)
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
