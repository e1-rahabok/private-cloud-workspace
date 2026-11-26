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
    k.begin(1060, 250)
    k.t(20, 26, "The method: seven steps and the loop back", 16, "bold")
    k.legend(20, 40, [("Before building, then kept current", "method"), ("Repeated for every slice", "prod")])
    steps = [("1. Map", ["SYSTEM.md", "intent.md"]), ("2. Interview", ["OPEN-QUESTIONS"]),
             ("3. Seams, owners", ["CONTRACTS.md", "DECISIONS.md"]), ("4. Requirements", ["requirements/"]),
             ("5. Checks", ["checks/, tools/"]), ("6. Slices", ["ROADMAP.md"]), ("7. Run", ["CLAUDE.md"])]
    w, gap, y, h = 130, 18, 76, 74
    for i, (title, lines) in enumerate(steps):
        x = 20 + i * (w + gap)
        k.box(x, y, w, title, lines, "method" if i < 4 else "prod", h=h)
        if i:
            k.arrow([(x - gap, y + h / 2), (x, y + h / 2)])
    first, last = 20 + w / 2, 20 + 6 * (w + gap) + w / 2
    k.arrow([(last, y + h), (last, 210), (first, 210), (first, y + h)],
            "Corrections, answers and new decisions go back into the files", 530, 214)
    k.finish(str(ROOT / "images" / "method.svg"))


def isvara_site_map() -> None:
    """spec/design/isvara-revamp.md: why visitors come, and the features behind each reason."""
    reasons = [
        ("Read", ["Articles: one topic, about 10 minutes", "Books: ordered paths through articles",
                  "Infographics: interactive SVG", "Guide: by object, technology, task"]),
        ("Ask", ["Chat with Agent E2, sources to the section", "Ask about this page",
                 "CSV and screenshot attachments", "MCP endpoint for other AI tools"]),
        ("Listen", ["Podcast: episodes per book chapter", "Transcripts and an RSS feed"]),
        ("Solve", ["Calculators from the catalog", "RVTools health check"]),
        ("Catch up", ["What's New: added, changed, corrected", "RSS feed"]),
        ("Fork", ["Manual: clone the base privately", "Add your organisation's content"]),
        ("Find", ["Search: plain words or regular expressions", "Metric finder, symptoms, glossary",
                  "Common misreadings"]),
        ("Practice", ["Fun Quiz: rounds, progress, a board", "Exam: ten very hard questions",
                      "2am game", "Self-assessment"]),
        ("Engage", ["Survey: feedback and session requests", "Thumbs up and down on answers"]),
        ("Download", ["The books and spreadsheets", "Weekly refresh of the downloads"]),
    ]
    w, gap, row = 450, 20, 112
    k.begin(960, 60 + 5 * row)
    k.t(20, 30, "isvara.io: why visitors come, and what serves each reason", 16, "bold")
    k.t(20, 50, "Every feature comes from Agent E2's knowledge; isvara.io holds none of its own.", 11.5, "normal", "#555")
    for i, (reason, lines) in enumerate(reasons):
        x = 20 + (i % 2) * (w + gap)
        y = 66 + (i // 2) * row
        k.box(x, y, w, reason, lines, "method" if i % 2 == 0 else "shared", h=row - 14)
    k.finish(str(ROOT / "images" / "isvara-site-map.svg"))


def roadmap() -> None:
    """ROADMAP.md: the milestones of release 1.0, their state and what each depends on."""
    k.begin(1060, 500)
    k.t(20, 26, "Release 1.0: milestones and what each depends on", 16, "bold")
    k.legend(20, 40, [("Done", "prod"), ("In progress", "guest"), ("Not started", "white")])
    w, h = 180, 70

    def b(x, y, title, lines, kind):
        k.box(x, y, w, title, lines, kind, h=h)

    b(20, 80, "M0 Workspace", ["Files, checks, tutorial"], "prod")
    b(20, 190, "M1 Specification", ["Intent, model, requirements;", "approval"], "guest")
    b(230, 190, "M2 Contracts, clean-up", ["KPI definitions, docs,", "Agent E2 plan"], "white")
    b(440, 190, "M8 Adapter identity", ["New name, data states"], "white")
    b(650, 190, "M9 Lab build", ["Nested hosts with tiering"], "white")
    b(440, 300, "M10 Agent E2 stage 1", ["Grader, progress, files,", "Day 2 scope"], "white")
    b(650, 80, "M3 Live demo: one KPI", ["One cluster, live"], "white")
    b(860, 80, "M4 Live demo: the rest", ["L2 performance, capacity"], "white")
    b(650, 410, "M5 isvara.io content", ["Paths, articles, search,", "infographics, tools"], "white")
    b(860, 300, "M6 isvara.io Ask", ["Agent E2, contributions,", "protection"], "white")
    b(860, 410, "M7 isvara.io Practice", ["Quiz, mastery map, exam"], "white")

    k.arrow([(110, 150), (110, 190)])
    k.arrow([(200, 225), (230, 225)])
    k.arrow([(410, 205), (420, 205), (420, 115), (650, 115)])
    k.arrow([(410, 225), (440, 225)])
    k.arrow([(410, 245), (425, 245), (425, 335), (440, 335)])
    k.arrow([(410, 255), (430, 255), (430, 445), (650, 445)])
    k.arrow([(830, 115), (860, 115)])
    k.arrow([(620, 225), (650, 225)])
    k.arrow([(530, 190), (530, 170), (940, 170), (940, 150)])
    k.arrow([(620, 320), (845, 320), (845, 160), (880, 160), (880, 150)])
    k.arrow([(620, 350), (860, 350)])
    k.arrow([(740, 410), (740, 390), (950, 390), (950, 370)])
    k.arrow([(830, 445), (860, 445)])
    k.finish(str(ROOT / "images" / "roadmap.svg"))


if __name__ == "__main__":
    system()
    method()
    isvara_site_map()
    roadmap()
