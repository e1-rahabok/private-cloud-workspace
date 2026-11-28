# /// script
# requires-python = ">=3.10"
# ///
"""Check of lab addresses: no repository holds a private network address outside the project's example network.

R-WS-010 (DESIGN-9): a real address of the lab, the author's laptop or a customer is never written in a repository.
The rule searches the tracked text files of every clone for IPv4 addresses in the private ranges of RFC 1918
(10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) and fails on any outside the example network 10.20.0.0/16, which the
synthetic demo, the sample estates and every written example use. Addresses in RFC 5737's documentation ranges and
public addresses are not private and pass.

A host name cannot be recognised by a pattern. When the environment variable LAB_PRIVATE_NAMES holds a
comma-separated list (on the author's laptop, from `$HOME\\.secrets\\lab.json`), every name in it fails too; the list
itself is never committed.

Outside the rule: the author's books as isvara.io serves them (`content/books/` in isvara), which are published as
they are, and this check and its planted breaks, which name the private ranges. A repository with no clone is reported as not run: isvara is private,
and its own CI runs this check (R-WS-002). checks/test_lab_addresses.py plants a break of each kind.
Exit 0: no problem. Exit 1: a problem. Exit 2: no repository could be read.
"""
from __future__ import annotations

import argparse
import ipaddress
import os
import re
import subprocess
import sys
from pathlib import Path

REPOS = ["private-cloud-workspace", "agent-e2", "PCM-Adapter", "private-cloud-manager", "isvara"]
EXAMPLE_NETWORK = ipaddress.ip_network("10.20.0.0/16")
PRIVATE = [ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")]
OUTSIDE = {
    "isvara": ["content/books/"],
    "private-cloud-workspace": ["checks/lab_addresses.py", "checks/test_lab_addresses.py"],
}
ADDRESS = re.compile(r"(?<![\d.])(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(?!\.?\d)")
PREFILTER = r"(^|[^0-9.])(10|172|192)\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"


def private_names() -> list[str]:
    return [n.strip() for n in os.environ.get("LAB_PRIVATE_NAMES", "").split(",") if n.strip()]


def is_lab_address(text: str) -> bool:
    try:
        address = ipaddress.ip_address(text)
    except ValueError:
        return False
    return any(address in n for n in PRIVATE) and address not in EXAMPLE_NETWORK


def problems_in(repo: str, clone: Path, names: list[str] | None = None) -> list[str]:
    names = private_names() if names is None else names
    pattern = PREFILTER + "".join("|" + re.escape(n) for n in names)
    out = subprocess.run(["git", "-C", str(clone), "grep", "-I", "-n", "-i", "-E", pattern],
                         capture_output=True, text=True).stdout
    problems = []
    for line in out.split("\n"):
        if not line or line.count(":") < 2:
            continue
        path, number, text = line.split(":", 2)
        if any(path.startswith(p) for p in OUTSIDE.get(repo, [])):
            continue
        # The value itself is never printed: the report names the file and line only.
        if any(is_lab_address(m.group(0)) for m in ADDRESS.finditer(text)):
            problems.append(f"{repo}: {path}:{number} holds a private address outside {EXAMPLE_NETWORK} (R-WS-010)")
        elif any(n.lower() in text.lower() for n in names):
            problems.append(f"{repo}: {path}:{number} holds a name from LAB_PRIVATE_NAMES (R-WS-010)")
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
    names = "with" if private_names() else "without"
    print(f"Lab addresses: {read} repositories read, {names} LAB_PRIVATE_NAMES, {len(problems)} problem(s)")
    if read == 0:
        return 2
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
