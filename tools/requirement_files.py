"""Where each repository keeps its requirement files (DESIGN-4), for the tools that read them all.

The workspace keeps the requirements on contracts, their checks and its own tools; every other requirement
lives in the repository that implements it. The child repositories are read from clones next to this one,
as for checks/run_all.py.

    from requirement_files import add_repos_argument, files
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = "e1-rahabok"
WORKSPACE = "private-cloud-workspace"
# Repository -> folder of its requirement files. agent-e2 keeps them under project/, by its own layout.
FOLDERS = {
    WORKSPACE: "spec/requirements",
    "agent-e2": "project/requirements",
    "PCM-Adapter": "spec/requirements",
    "private-cloud-manager": "spec/requirements",
    "isvara": "spec/requirements",
}
CHILDREN = [r for r in FOLDERS if r != WORKSPACE]


@dataclass(frozen=True)
class ReqFile:
    repo: str
    path: Path

    @property
    def name(self) -> str:
        """The name a problem report uses: the file, with its repository when it is not the workspace."""
        return self.path.name if self.repo == WORKSPACE else f"{self.repo}/{FOLDERS[self.repo]}/{self.path.name}"

    def link(self, from_review_page: bool = True) -> str:
        """A link to the file: relative from spec/review inside the workspace, a GitHub URL elsewhere."""
        if self.repo == WORKSPACE:
            return f"../requirements/{self.path.name}" if from_review_page else f"spec/requirements/{self.path.name}"
        return f"https://github.com/{OWNER}/{self.repo}/blob/main/{FOLDERS[self.repo]}/{self.path.name}"


def add_repos_argument(ap: argparse.ArgumentParser) -> None:
    ap.add_argument("--repos", nargs="*", default=CHILDREN,
                    help="child repositories to read (default: all); CI names the ones it can read")


def files(repos: list[str]) -> tuple[list[ReqFile], list[str], list[str]]:
    """The requirement files of the workspace and of the named child repositories; the child repositories
    not named (reported as not run); and the named ones with no clone (the tool could not run)."""
    out = [ReqFile(WORKSPACE, p) for p in sorted((ROOT / FOLDERS[WORKSPACE]).glob("*.md")) if p.name != "README.md"]
    unread, missing = [], []
    for repo in CHILDREN:
        if repo not in repos:
            unread.append(repo)
            continue
        clone = ROOT.parent / repo
        if not clone.is_dir():
            missing.append(repo)
            continue
        folder = clone / FOLDERS[repo]
        out += [ReqFile(repo, p) for p in sorted(folder.glob("*.md")) if p.name != "README.md"]
    return out, unread, missing
