# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "requests"]
# ///
"""Run every cross-repo check against clones of the repositories: the contract checks here (the contracts in spec/design/system.md), then the name checks of R-WS-007, R-REPO-006, R-REPO-007 and R-REPO-008, the lab address check of R-WS-010, and the secret and workflow checks of R-WS-011 and R-WS-012, in tools/.

The clones sit next to this repository by default:

    <folder>/private-cloud-workspace   (this repository)
    <folder>/agent-e2
    <folder>/PCM-Adapter
    <folder>/private-cloud-manager

A missing clone is cloned from GitHub (depth 1), unless --no-clone. --pull updates the existing
clones to their default branch first; without it the checks run on what the clones hold, which is
how you test a branch of a child repository before you merge it.

Exit 0 when every check passes, 1 when one fails, 2 when one could not run.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

OWNER = "e1-rahabok"
HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent / "tools"
# (title, script, the clones it needs). The name checks also read isvara when its clone is there, and report it as
# not run otherwise: isvara is private, and its own CI runs them (R-WS-002).
CHECKS = [
    ("C1 KPI definitions", HERE / "kpi_definitions.py", ["agent-e2", "PCM-Adapter"]),
    ("C3 Agent E2 API", HERE / "agent_e2_api.py", ["agent-e2", "private-cloud-manager"]),
    ("R-WS-007 file names", TOOLS / "file_names.py", ["agent-e2", "PCM-Adapter", "private-cloud-manager"]),
    ("Forbidden names", TOOLS / "forbidden_names.py", ["agent-e2", "PCM-Adapter", "private-cloud-manager"]),
    ("R-WS-010 lab addresses", TOOLS / "lab_addresses.py", ["agent-e2", "PCM-Adapter", "private-cloud-manager"]),
    ("R-WS-011 secrets", TOOLS / "secret_values.py", ["agent-e2", "PCM-Adapter", "private-cloud-manager"]),
    ("R-WS-012 and R-WS-014 workflows, Dependabot, branch cleanup", TOOLS / "workflows.py", ["agent-e2", "PCM-Adapter", "private-cloud-manager"]),
]


def prepare(repos: Path, names: set[str], clone: bool, pull: bool) -> bool:
    ok = True
    for name in sorted(names):
        path = repos / name
        if path.is_dir():
            if pull:
                subprocess.run(["git", "-C", str(path), "pull", "--ff-only", "-q"], check=False)
        elif clone:
            print(f"Cloning {OWNER}/{name} ...")
            r = subprocess.run(["git", "clone", "-q", "--depth", "1", f"https://github.com/{OWNER}/{name}.git", str(path)])
            ok &= r.returncode == 0
        else:
            print(f"ERROR: {path} not found")
            ok = False
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repos", type=Path, default=HERE.parents[1], help="folder that holds the clones")
    parser.add_argument("--no-clone", action="store_true", help="fail instead of cloning a missing repository")
    parser.add_argument("--pull", action="store_true", help="update existing clones first")
    args = parser.parse_args()
    if not prepare(args.repos, {r for _, _, rs in CHECKS for r in rs}, not args.no_clone, args.pull):
        return 2
    worst = 0
    for title, script, _ in CHECKS:
        print(f"\n== {title}", flush=True)
        code = subprocess.run([sys.executable, str(script), "--repos", str(args.repos)]).returncode
        worst = max(worst, code)
    print("\nAll checks passed." if worst == 0 else
          f"\nAt least one check {'failed' if worst == 1 else 'could not run'}.")
    return worst


if __name__ == "__main__":
    sys.exit(main())
