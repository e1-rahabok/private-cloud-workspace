"""Writing style of the documents in this repository.

The rules are Agent E2's, kept in one place:
- agent-e2/project/knowledge-rules/writing.md: the rules;
- agent-e2/project/tools/rules_check_values.yaml, avoid_ai_speak: the flagged phrases, read from the
  clone next to this repository.

Documents fall into two groups (WD-023 in DECISIONS.md):
- For people: plain prose. Checked for flagged phrases, sentence headings (questions, How/Why/What
  openers), long headings, and tables too wide or too wordy for GitHub.
- For machines: CLAUDE.md files, requirements and templates. Optimised for an agent to follow, so only the
  flagged phrases are checked; their headings may be claims (a requirement title states a behaviour).
Records kept verbatim (the interview's answers) are not checked.

Known style debt (STYLE_DEBT below) is a baseline: a listed file is reported as KNOWN and does not fail.
The list may only shrink: a listed file that has become clean fails until it is removed from the list.

What no pattern finds (slogans, "X, not Y", hedging, praise) is left to review: read each changed line
with the lines around it.

    python tools/style.py      # exit 1 on any problem
"""
from __future__ import annotations

import re
import sys
from fnmatch import fnmatch
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT.parent / "agent-e2" / "project" / "tools" / "rules_check_values.yaml"

MACHINE = ["CLAUDE.md", "*/CLAUDE.md", "spec/requirements/*", "tutorial/templates/*"]
VERBATIM = ["spec/interview-round-*.md"]
# Files waiting for a rewrite that will fix their style; remove a line when the file is clean.
STYLE_DEBT: dict[str, str] = {}
OPENER = re.compile(r"(How|Why|What|When|Where|Which|Who)\b")
HEADING = re.compile(r"^(#{1,4}) (.+)$")
FENCE = re.compile(r"^```.*?^```", re.S | re.M)
DETAILS = re.compile(r"<details>.*?</details>", re.S)


def group(rel: str) -> str:
    if any(fnmatch(rel, g) for g in VERBATIM):
        return "verbatim"
    if any(fnmatch(rel, g) for g in MACHINE):
        return "machine"
    return "people"


def phrases() -> dict[str, str]:
    data = yaml.safe_load(RULES.read_text(encoding="utf-8"))
    return data.get("avoid_ai_speak") or {}


def check_headings(rel: str, lines: list[str], problems: list[str]) -> None:
    questions_file = rel == "OPEN-QUESTIONS.md"
    for i, line in enumerate(lines, 1):
        m = HEADING.match(line)
        if not m:
            continue
        level, text = m.group(1), m.group(2).strip()
        if questions_file and text.startswith("Q-"):
            continue  # an interview question is a question by design
        text = re.sub(r"^\d+\.\s+", "", text)  # chapter numbers
        bare = re.sub(r"\([^)]*\)|`[^`]*`|\[([^\]]*)\]\([^)]*\)", r"\1", text)
        words = len(bare.split())
        limit = 8 if level == "#" else 9
        if words > limit:
            problems.append(f"{rel}:{i}: heading of {words} words, at most {limit}: name the topic")
        if OPENER.match(bare) or bare.endswith("?"):
            problems.append(f"{rel}:{i}: sentence heading \"{text}\": use a noun phrase that names the topic")


def check_tables(rel: str, lines: list[str], problems: list[str]) -> None:
    for i, line in enumerate(lines, 1):
        if not line.startswith("|") or re.match(r"^\|[\s:|-]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        texty = [c for c in cells if len(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", c).split()) > 3]
        if len(cells) > 4 and texty:
            problems.append(f"{rel}:{i}: table of {len(cells)} columns with text; at most 4, or use bullets")
        for c in cells:
            n = len(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", c).split())
            if n > 16:
                problems.append(f"{rel}:{i}: table cell of {n} words; keep cells short (about 12) or use bullets")
                break


def main() -> int:
    flagged = {re.compile(p): use for p, use in phrases().items()}
    problems: list[str] = []
    known: list[str] = []
    files = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
    for f in sorted(files):
        rel = f.relative_to(ROOT).as_posix()
        kind = group(rel)
        if kind == "verbatim":
            continue
        blank = lambda m: "\n" * m.group(0).count("\n")  # keep line numbers
        text = DETAILS.sub(blank, FENCE.sub(blank, f.read_text(encoding="utf-8")))
        before = len(problems)
        lines = text.split("\n")
        for i, line in enumerate(lines, 1):
            for pat, use in flagged.items():
                m = pat.search(line)
                if m:
                    problems.append(f"{rel}:{i}: \"{m.group(0)}\": {use}")
        if kind == "people":
            check_headings(rel, lines, problems)
            check_tables(rel, lines, problems)
        if rel in STYLE_DEBT:
            found = len(problems) - before
            del problems[before:]
            if found:
                known.append(f"{rel}: {found} problem(s), {STYLE_DEBT[rel]}")
            else:
                problems.append(f"{rel}: listed in STYLE_DEBT but now clean: remove it from the list")
    for k in known:
        print(f"KNOWN {k}")
    for p in problems:
        print(f"FAIL {p}")
    print(f"style: {len(files)} Markdown files, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
