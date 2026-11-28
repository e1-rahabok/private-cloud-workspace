# /// script
# requires-python = ">=3.10"
# ///
"""Check of secrets: no repository holds a token, a private key or a password written as a value.

R-WS-011 (DESIGN-26): the tracked text files of every clone are searched for provider tokens (GitHub, OpenAI,
Anthropic, AWS, Slack, Vercel), private key blocks, and a password, secret, token or key assigned a quoted value.
A value that is a placeholder passes: it holds `...`, `<`, `$`, `{`, "example", "changeme", "placeholder", "your",
"xxx", "dummy", "fake" or "test", or it is the sample password of a vendor's example file (VMware1!).

isvara is private on a free plan, where GitHub runs no secret scanning, so this check is the one that covers it there;
the public repositories also have GitHub's secret scanning and push protection. A repository with no clone is reported
as not run. The report names the file, the line and the kind, never the value. tools/test_secret_values.py plants a break
of each kind. Exit 0: no problem. Exit 1: a problem. Exit 2: no repository could be read.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPOS = ["private-cloud-workspace", "agent-e2", "PCM-Adapter", "private-cloud-manager", "isvara"]
KINDS = [
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{30,}")),
    ("OpenAI or Anthropic key", re.compile(r"(?<![A-Za-z0-9-])sk-(?:ant-|proj-)?[A-Za-z0-9_-]{24,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}")),
    ("Vercel token", re.compile(r"\bvc[kp]_[A-Za-z0-9]{20,}")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----")),
    ("password or key written as a value", re.compile(r"""(?i)\b(?:password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key)\b["']?\s*[:=]\s*["']([^"'\s]{6,})["']""")),
]
PLACEHOLDER = re.compile(r"(?i)\.\.\.|[<>${}]|example|changeme|placeholder|your|xxx|dummy|fake|test|redacted|VMware1!")
OUTSIDE = {"private-cloud-workspace": ["tools/test_secret_values.py"]}
PREFILTER = (r"gh[pousr]_|github_pat_|sk-|AKIA|xox[abpr]-|vc[kp]_|PRIVATE KEY-----"
             r"|(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key)[\"']?[[:space:]]*[:=]")


def problems_in(repo: str, clone: Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(clone), "grep", "-I", "-n", "-i", "-E", PREFILTER],
                         capture_output=True, text=True).stdout
    problems = []
    for line in out.split("\n"):
        if not line or line.count(":") < 2:
            continue
        path, number, text = line.split(":", 2)
        if any(path.startswith(p) for p in OUTSIDE.get(repo, [])):
            continue
        for kind, rule in KINDS:
            found = [m for m in rule.finditer(text) if not PLACEHOLDER.search(m.group(m.lastindex or 0))]
            if found:
                problems.append(f"{repo}: {path}:{number} holds what looks like a {kind} (R-WS-011)")
                break
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
    print(f"Secrets: {read} repositories read, {len(problems)} problem(s)")
    if read == 0:
        return 2
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
