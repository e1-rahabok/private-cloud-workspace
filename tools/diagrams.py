"""Draw the SVG diagrams of this repository.

Diagrams are drawn by code, never by hand, with the drawing kit of Agent E2
(agent-e2/project/tools/diagram_kit.py, read from the clone next to this repository). The text a
machine reads is generated from each SVG by tools/docs.py and placed under the image.

    python tools/diagrams.py        # redraw every diagram into images/
    python tools/docs.py            # then refresh the text under each image
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "agent-e2" / "project" / "tools"))
import diagram_kit as k  # noqa: E402


def system() -> None:
    """SYSTEM.md: the parts, where they run, and the contracts between them."""
    # No group frames: the text generator reads every text inside a rectangle as part of it, so an
    # arrow label inside a frame would be lost. Where a part runs is written in its own box.
    k.begin(960, 490)
    k.t(20, 30, "The system, stage 1", 16, "bold")
    k.legend(20, 44, [("PCM", "data"), ("Agent E2", "method"), ("PCM-Adapter", "prod"),
                      ("isvara.io", "shared"), ("Model", "guest")])
    k.t(700, 56, "Dashed: planned", 11.5, "normal", "#555")

    k.box(20, 90, 250, "PCM", ["Web app for operations roles;", "synthetic ACME or live data;", "lab VM, https://10.114.1.29"], "data")
    k.box(350, 90, 250, "Agent E2 for PCM", ["Knowledge service over HTTP;", "owns all domain knowledge;", "same lab VM, port 8090"], "method")
    k.box(20, 300, 300, "VCF Operations", ["Lab, https://10.115.1.81"], "white", h=180)
    k.box(40, 370, 260, "PCM-Adapter", ["Computes the KPIs inside VCF", "Operations, under vCommunity|"], "prod")

    k.box(680, 90, 260, "isvara.io", ["Public learning site;", "on Vercel; no live system"], "shared")
    k.box(680, 230, 260, "Agent E2 for isvara.io", ["Where it runs: OPEN-QUESTIONS Q-4"], "method", dash=True)
    k.box(680, 390, 260, "Vercel AI Gateway", ["Cloud model for stage 1"], "guest")

    k.arrow([(270, 130), (350, 130)], "C3", 310, 123)
    k.arrow([(145, 171), (145, 300)], "C2 Suite API, live mode", 145, 240)
    k.arrow([(475, 171), (475, 410), (300, 410)], "C1 KPI definitions", 475, 300, dash=True)
    k.arrow([(600, 150), (640, 150), (640, 415), (680, 415)], "C5", 640, 300)
    k.arrow([(600, 110), (680, 110)], "C4", 640, 103, dash=True)
    k.arrow([(810, 156), (810, 230)], "C3", 810, 197, dash=True)
    k.arrow([(810, 281), (810, 390)], "C5", 810, 340, dash=True)
    k.finish(str(ROOT / "images" / "system.svg"))


def method() -> None:
    """tutorial/02-the-method.md: the six steps and the loop back."""
    k.begin(960, 230)
    k.t(20, 26, "The method: six steps and the loop back", 16, "bold")
    k.legend(20, 40, [("Written once, kept current", "method"), ("Repeated for every slice", "prod")])
    steps = [("1. Map", "SYSTEM.md"), ("2. Seams", "CONTRACTS.md"), ("3. Owners", "DECISIONS.md"),
             ("4. Done", "ROADMAP.md"), ("5. Slices", "ROADMAP.md"), ("6. Run", "checks, CLAUDE.md")]
    w, gap, y = 135, 22, 76
    for i, (title, line) in enumerate(steps):
        x = 20 + i * (w + gap)
        k.box(x, y, w, title, [line], "method" if i < 4 else "prod", h=58)
        if i:
            k.arrow([(x - gap, y + 29), (x, y + 29)])
    first, last = 20 + w / 2, 20 + 5 * (w + gap) + w / 2
    k.arrow([(last, y + 58), (last, 190), (first, 190), (first, y + 58)],
            "Corrections, answers and new decisions go back into the files", 480, 194)
    k.finish(str(ROOT / "images" / "method.svg"))


if __name__ == "__main__":
    system()
    method()
