# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Check of workflows and dependency updates: least rights, pinned actions, and Dependabot for every package system.

R-WS-012 (DESIGN-25, DESIGN-26), in the tracked files of every clone:
- every workflow in `.github/workflows/` declares `permissions` at its top level;
- every `uses:` names an action of `actions/` (GitHub's own, by major version), a local path, a workflow of this
  workspace, or any other action by its full 40-character commit hash;
- `.github/dependabot.yml` exists and has an update entry for `github-actions`, one for `npm` when a
  `package-lock.json` is tracked, and one for `pip` when a `requirements.txt` is tracked, in that file's folder.

A repository with no clone is reported as not run. tools/test_workflows.py plants a break of each kind.
Exit 0: no problem. Exit 1: a problem. Exit 2: no repository could be read.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPOS = ["private-cloud-workspace", "agent-e2", "PCM-Adapter", "private-cloud-manager", "isvara"]
OWN = re.compile(r"^(?:actions/[\w.-]+@v\d+|\./.+|e1-rahabok/private-cloud-workspace/\.github/workflows/[\w.-]+@main)$")
PINNED = re.compile(r"^[\w.-]+/[\w./-]+@[0-9a-f]{40}$")
USES = re.compile(r"^\s*-?\s*uses:\s*['\"]?([^'\"\s#]+)")


def tracked(clone: Path) -> list[str]:
    return subprocess.run(["git", "-C", str(clone), "ls-files"], capture_output=True, text=True).stdout.split("\n")


def ecosystems(clone: Path) -> dict[tuple[str, str], bool]:
    path = clone / ".github" / "dependabot.yml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    found = {}
    for u in data.get("updates", []) or []:
        folder = "/" + str(u.get("directory", "/")).strip("/")
        found[(u.get("package-ecosystem"), folder.rstrip("/") or "/")] = True
    return found


def problems_in(repo: str, clone: Path) -> list[str]:
    problems = []
    files = tracked(clone)
    for f in files:
        if not re.match(r"^\.github/workflows/[^/]+\.ya?ml$", f):
            continue
        text = (clone / f).read_text(encoding="utf-8")
        data = yaml.safe_load(text) or {}
        if "permissions" not in data:
            problems.append(f"{repo}: {f} declares no top-level permissions (R-WS-012)")
        for number, line in enumerate(text.split("\n"), 1):
            if line.lstrip().startswith("#"):
                continue
            m = USES.match(line)
            if m and not (OWN.match(m.group(1)) or PINNED.match(m.group(1))):
                problems.append(f"{repo}: {f}:{number} uses '{m.group(1)}', not pinned to a commit hash (R-WS-012)")
    found = ecosystems(clone)
    if not (clone / ".github" / "dependabot.yml").exists():
        problems.append(f"{repo}: .github/dependabot.yml is missing (R-WS-012)")
        return problems
    if not any(e == "github-actions" for e, _ in found):
        problems.append(f"{repo}: .github/dependabot.yml has no github-actions entry (R-WS-012)")
    for f in files:
        name = f.rsplit("/", 1)[-1]
        system = {"package-lock.json": "npm", "requirements.txt": "pip"}.get(name)
        if system:
            folder = "/" + (f.rsplit("/", 1)[0] if "/" in f else "")
            folder = folder.rstrip("/") or "/"
            if (system, folder) not in found:
                problems.append(f"{repo}: {f} has no {system} entry for '{folder}' in .github/dependabot.yml (R-WS-012)")
    return problems


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
        problems += problems_in(repo, clone)
    for repo in not_run:
        print(f"NOT RUN {repo}: no clone")
    for p in problems:
        print(f"FAIL {p}")
    print(f"Workflows: {read} repositories read, {len(problems)} problem(s)")
    if read == 0:
        return 2
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
