"""Keep the Markdown of this repository readable by people and by machines.

Three rules, the same as in agent-e2:
1. A file reference is a link. A backticked path that exists, here or in one of the child
   repositories, becomes [`path`](link): relative inside this repository, a full GitHub URL for a
   child repository. GitHub makes it clickable. A path that exists in more than one child
   repository is reported, to be linked by hand.
2. A diagram is an SVG drawn by tools/diagrams.py, with its text under the image in a
   <details> block, generated from the SVG by agent-e2's diagram_text.py. Never edit that block.
3. Every relative link resolves.

    python tools/docs.py           # add missing links and refresh the diagram text
    python tools/docs.py --check   # report instead of writing; exit 1 on any problem (CI)

Reads the child repositories from clones next to this one.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
OWNER = "e1-rahabok"
CHILDREN = ["agent-e2", "PCM-Adapter", "private-cloud-management", "isvara"]
sys.path.insert(0, str(PARENT / "agent-e2" / "project" / "tools"))
from diagram_text import svg_to_text  # noqa: E402

SUMMARY = "Text of the diagram, for readers that cannot see it"
IMAGE = re.compile(r"(!\[[^\]]*\]\(([^)\s]+\.svg)\)\n)(?:\n?<details>\n<summary>Text of the diagram.*?</details>\n)?", re.S)
TICK = re.compile(r"(?<!\[)`([\w.*/-]+)`(?!\]\()")
FENCE = re.compile(r"^```.*?^```", re.S | re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")


def markdown_files() -> list[Path]:
    return [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]


def looks_like_path(ref: str) -> bool:
    return "/" in ref or bool(re.search(r"\.(md|py|ya?ml|json|ps1|sql|ts|tsx|mjs|svg|csv)$", ref))


def resolve(ref: str, doc: Path) -> tuple[str | None, str | None]:
    """(link, problem) for a backticked reference. Globs link to their folder."""
    path = ref.rstrip("/")
    if "*" in path:
        path = path.rsplit("/", 1)[0] if "/" in path else ""
    if not path:
        return None, None
    here = ROOT / path
    if here.exists():
        return os.path.relpath(here, doc.parent).replace(os.sep, "/"), None
    hits = [r for r in CHILDREN if (PARENT / r / path).exists()]
    if len(hits) == 1:
        kind = "tree" if (PARENT / hits[0] / path).is_dir() else "blob"
        return f"https://github.com/{OWNER}/{hits[0]}/{kind}/main/{path}", None
    if len(hits) > 1:
        return None, f"`{ref}` exists in {', '.join(hits)}: link it by hand"
    return None, None


def link_paths(text: str, doc: Path, problems: list[str]) -> str:
    parts, last = [], 0
    for m in FENCE.finditer(text):
        parts.append((text[last:m.start()], True))
        parts.append((m.group(0), False))
        last = m.end()
    parts.append((text[last:], True))

    def repl(m):
        ref = m.group(1)
        if not looks_like_path(ref) or ref.startswith("/"):
            return m.group(0)
        link, problem = resolve(ref, doc)
        if problem:
            problems.append(f"{doc.relative_to(ROOT)}: {problem}")
        return f"[`{ref}`]({link})" if link else m.group(0)

    return "".join(TICK.sub(repl, chunk) if prose else chunk for chunk, prose in parts)


def diagram_text(text: str, doc: Path, problems: list[str]) -> str:
    def repl(m):
        svg = (doc.parent / m.group(2)).resolve()
        if not svg.exists():
            problems.append(f"{doc.relative_to(ROOT)}: image {m.group(2)} not found")
            return m.group(0)
        return f"{m.group(1)}\n<details>\n<summary>{SUMMARY}</summary>\n\n{svg_to_text(str(svg))}\n\n</details>\n"
    return IMAGE.sub(repl, text)


def broken_links(text: str, doc: Path) -> list[str]:
    bad = []
    for link in LINK.findall(FENCE.sub("", text)):
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if not (doc.parent / link.split("#")[0]).exists():
            bad.append(f"{doc.relative_to(ROOT)}: broken link {link}")
    return bad


def main() -> int:
    write = "--check" not in sys.argv
    problems: list[str] = []
    for doc in markdown_files():
        old = doc.read_text(encoding="utf-8")
        new = diagram_text(link_paths(old, doc, problems), doc, problems)
        problems += broken_links(new, doc)
        if new != old:
            if write:
                doc.write_text(new, encoding="utf-8")
                print(f"updated {doc.relative_to(ROOT)}")
            else:
                problems.append(f"{doc.relative_to(ROOT)}: unlinked file reference or stale diagram text (run python tools/docs.py)")
    for p in problems:
        print(f"FAIL {p}")
    print(f"docs: {len(markdown_files())} Markdown files, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
