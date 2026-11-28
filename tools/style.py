"""Writing style of the documents of every repository (R-WS-006).

The rules are held once, in this workspace ([writing/README.md](../writing/README.md)); the flagged phrases are
writing/flagged-phrases.yaml. Documents fall into three groups (GROUPS below, per repository):
- For people: plain prose. Checked for flagged phrases, sentence headings (questions, How/Why/What openers), long
  headings, and tables too wide or too wordy for GitHub.
- For machines: CLAUDE.md and CLAUDE-PROJECT.md files, requirements, templates and Agent E2's knowledge files.
  Optimised for an agent or a model, so only the flagged phrases are checked.
- Records kept as they were said or written (interview answers, the author's books and papers, dated reviews):
  not checked.

Known style debt is a baseline in each repository, style-baseline.yaml at its root (file -> number of problems): a
listed file is reported as KNOWN while it has its listed number of problems. The baseline may only shrink: a file with
more problems fails, and so does a file with fewer until the same pull request lowers its number or, when clean,
removes it. A repository's baseline goes with a question in that repository's question file (DESIGN-23). A repository
without the file is not checked yet, and the check says so.

What no pattern finds (slogans, "X, not Y", hedging, praise) is left to review: read each changed line with the
lines around it.

    python tools/style.py                  # this workspace; exit 1 on any problem
    python tools/style.py --repo isvara    # a child repository's clone next to this one
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PHRASES = ROOT / "writing" / "flagged-phrases.yaml"
BASELINE = "style-baseline.yaml"  # at the root of each repository
WORKSPACE = "private-cloud-workspace"

COMMON_MACHINE = ["CLAUDE.md", "*/CLAUDE.md", "CLAUDE-PROJECT.md", "spec/requirements/*", "project/requirements/*"]
# Per repository: (documents for machines, records kept verbatim), as fnmatch patterns on the repository path.
GROUPS = {
    WORKSPACE: (["tutorial/templates/*"], ["spec/author-input/*"]),
    "agent-e2": (["knowledge/*", "benchmark/questions/*", "benchmark/_templates/*", "project/templates/*"],
                 ["project/author-questions-resolved.md", "benchmark/results/*", "project/sources/*",
                  "project/*-20[0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"]),  # dated records
    "PCM-Adapter": (["Management Pack/content/*"], ["docs/development-guide/engineering-review/*"]),
    "private-cloud-manager": ([], ["author-papers/*"]),
    "isvara": ([], ["content/*", "node_modules/*"]),
}
OPENER = re.compile(r"(How|Why|What|When|Where|Which|Who)\b")
HEADING = re.compile(r"^(#{1,4}) (.+)$")
FENCE = re.compile(r"^```.*?^```", re.S | re.M)
DETAILS = re.compile(r"<details>.*?</details>", re.S)


def group(repo: str, rel: str) -> str:
    machine, verbatim = GROUPS.get(repo, ([], []))
    if any(fnmatch(rel, g) for g in verbatim):
        return "verbatim"
    if any(fnmatch(rel, g) for g in COMMON_MACHINE + machine):
        return "machine"
    return "people"


def phrases() -> dict[str, str]:
    data = yaml.safe_load(PHRASES.read_text(encoding="utf-8"))
    return data.get("flagged_phrases") or {}


def baseline(root: Path) -> dict[str, int]:
    """The repository's known style debt: file -> number of problems."""
    return yaml.safe_load((root / BASELINE).read_text(encoding="utf-8")) or {}


def markdown_files(root: Path) -> list[str]:
    """The tracked Markdown files of a clone, as repository paths."""
    out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "*.md"], capture_output=True, text=True, check=True)
    return sorted(path for path in out.stdout.split("\0") if path)


def check_headings(rel: str, lines: list[str], problems: list[str]) -> None:
    questions_file = rel.endswith("OPEN-QUESTIONS.md") or rel == "project/author-questions.md"
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


def problems_of(repo: str, root: Path, rel: str, flagged: dict) -> list[str]:
    kind = group(repo, rel)
    if kind == "verbatim":
        return []
    blank = lambda m: "\n" * m.group(0).count("\n")  # keep line numbers
    text = DETAILS.sub(blank, FENCE.sub(blank, (root / rel).read_text(encoding="utf-8")))
    lines = text.split("\n")
    problems: list[str] = []
    for i, line in enumerate(lines, 1):
        for pat, use in flagged.items():
            m = pat.search(line)
            if m:
                problems.append(f"{rel}:{i}: \"{m.group(0)}\": {use}")
    if kind == "people":
        check_headings(rel, lines, problems)
        check_tables(rel, lines, problems)
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=WORKSPACE, help="the repository to check: this workspace or a clone next to it")
    args = ap.parse_args()
    root = ROOT if args.repo == WORKSPACE else ROOT.parent / args.repo
    if not (root / ".git").exists():
        print(f"COULD NOT RUN {args.repo}: no clone at {root}")
        return 2
    flagged = {re.compile(p): use for p, use in phrases().items()}
    if not (root / BASELINE).is_file():
        print(f"NOT RUN {args.repo}: no {BASELINE} yet; its first run and its question come first")
        return 0
    debt = baseline(root)
    problems: list[str] = []
    known: list[str] = []
    files = markdown_files(root)
    for rel in files:
        found = problems_of(args.repo, root, rel, flagged)
        if rel in debt:
            if len(found) > debt[rel]:
                problems += found
                problems.append(f"{rel}: {len(found)} problem(s), more than its baseline of {debt[rel]}")
            elif len(found) < debt[rel]:
                problems.append(f"{rel}: {len(found)} problem(s), fewer than its baseline of {debt[rel]}: "
                                + ("remove it from" if not found else f"lower it to {len(found)} in") + f" {BASELINE}")
            else:
                known.append(f"{rel}: {len(found)} problem(s) in the baseline")
        else:
            problems += found
    for rel in sorted(set(debt) - set(files)):
        problems.append(f"{rel}: in the baseline of {args.repo} but not a tracked file: remove it")
    for k in known:
        print(f"KNOWN {k}")
    for p in problems:
        print(f"FAIL {p}")
    print(f"style {args.repo}: {len(files)} Markdown files, {len(problems)} problem(s), {len(known)} file(s) in the baseline")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
