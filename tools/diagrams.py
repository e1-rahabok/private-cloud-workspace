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
    """spec/design/system.md: the parts, where they run, and the contracts between them."""
    # No group frames: the text generator reads every text inside a rectangle as part of it, so an
    # arrow label inside a frame would be lost. Where a part runs is written in its own box.
    k.begin(960, 490)
    k.t(20, 30, "The system, release 1.0", 16, "bold")
    k.legend(20, 44, [("PCM", "data"), ("Agent E2", "method"), ("VCF vCommunity Adapter", "prod"),
                      ("isvara.io", "shared"), ("Model", "guest")])
    k.t(560, 56, "Dashed: planned, or files with no call at run time", 11.5, "normal", "#555")

    k.box(20, 90, 250, "PCM", ["Web app for operations roles;", "synthetic ACME or live data;", "lab VM, https://10.114.1.29"], "data")
    k.box(350, 90, 250, "Agent E2 for PCM", ["Knowledge service over HTTP;", "owns all domain knowledge;", "same lab VM, port 8090"], "method")
    k.box(20, 300, 300, "VCF Operations", ["Lab, https://10.115.1.81"], "white", h=180)
    k.box(40, 370, 260, "VCF vCommunity Adapter", ["Computes the KPIs inside VCF", "Operations, under vCommunity|"], "prod")

    k.box(680, 90, 260, "isvara.io", ["Public learning site;", "on Vercel; no live system"], "shared")
    k.box(680, 230, 260, "Agent E2 for isvara.io", ["Where it runs: measured and chosen", "in M5 (Q-WS-4)"], "method", dash=True)
    k.box(680, 390, 260, "Vercel AI Gateway", ["Cloud model for release 1.0"], "guest")

    k.arrow([(270, 130), (350, 130)], "C3", 310, 123)
    k.arrow([(145, 171), (145, 300)], "C2 Suite API, scenario 7", 145, 240)
    k.arrow([(475, 171), (475, 410), (300, 410)], "C1 KPI definitions", 475, 300, dash=True)
    k.arrow([(600, 150), (640, 150), (640, 415), (680, 415)], "C5", 640, 300)
    k.arrow([(600, 110), (680, 110)], "C4 export", 640, 103, dash=True)
    k.arrow([(810, 156), (810, 230)], "C3", 810, 197, dash=True)
    k.arrow([(810, 296), (810, 390)], "C5", 810, 345, dash=True)
    k.finish(str(ROOT / "images" / "system.svg"))


def parts() -> None:
    """README.md: the five parts, who each is for, and what flows between them."""
    k.begin(960, 500)
    k.t(20, 30, "One body of knowledge, five parts", 16, "bold")
    k.legend(20, 44, [("By people, for people", "prod"), ("For AI to read", "method"),
                      ("For people, built with AI", "shared"), ("No AI", "white")])

    k.box(20, 90, 250, "The Book", ["Private Cloud Management: Executive", "Summary and 4 parts, with spreadsheets,", "slides, diagrams. By people, for people."], "prod")
    k.box(355, 230, 250, "Agent E2: the brain", ["Holds the knowledge, for AI to read.", "Answers questions; defines every", "KPI, threshold and metric name."], "method")
    k.box(690, 90, 250, "isvara.io", ["Public website for learning:", "articles, tools, practice, Ask.", "Articles written by AI from Agent E2.", "The Book to download."], "shared")
    k.box(690, 380, 250, "Private Cloud Manager (PCM)", ["Web app for operations teams.", "Shows the KPIs; Agent E2 explains", "them. A demo in release 1.0."], "shared")
    k.box(20, 380, 250, "VCF vCommunity Adapter", ["Management pack for VCF", "Operations. Calculates the", "Agent E2 KPIs; adds features.", "No AI."], "white")

    k.arrow([(270, 110), (690, 110)], "the Book to download", 480, 103)
    k.arrow([(145, 171), (145, 250), (355, 250)], "extracted; kept in agreement", 145, 215)
    k.arrow([(605, 250), (780, 250), (780, 186)], "articles; Ask Agent E2", 690, 243)
    k.arrow([(420, 311), (420, 428), (270, 428)], "KPI definitions, names", 345, 421)
    k.arrow([(540, 311), (540, 400), (690, 400)], "explains the KPIs", 615, 393)
    k.arrow([(270, 455), (690, 455)], "KPIs, read from VCF Operations", 480, 448)
    k.finish(str(ROOT / "images" / "parts.svg"))


def roadmap() -> None:
    """ROADMAP.md: the milestones of release 1.0, their state and what each depends on."""
    k.begin(1060, 410)
    k.t(20, 26, "Release 1.0: milestones and what each depends on", 16, "bold")
    k.legend(20, 40, [("Done", "prod"), ("In progress", "guest"), ("Not started", "white")])
    w, h = 190, 70

    def b(x, y, title, lines, kind):
        k.box(x, y, w, title, lines, kind, h=h)

    b(20, 80, "Claude's method", ["Rules, gate, hook;", "done before the milestones"], "prod")
    b(230, 80, "M1 Release 1.0 specified", ["Every requirement, isvara.io", "design; no code"], "prod")
    b(440, 80, "M2 Contracts, clean-up", ["Checks in every repository;", "names, PCM folders"], "guest")
    b(650, 80, "M3 Agent E2 for both", ["Jobs, files, sources,", "grader, Day 2 only"], "white")
    b(860, 80, "M8 PCM live demo", ["Adapter fixes, live L2;", "every lab test"], "white")
    b(440, 200, "M4 isvara.io reading", ["Export, articles, paths,", "search, infographics"], "white")
    b(650, 200, "M5 isvara.io Ask", ["Agent E2, contributions,", "protection"], "white")
    b(860, 200, "M7 isvara.io switch-over", ["Home, What's New, manual;", "old links redirected"], "white")
    b(650, 320, "M6 isvara.io practice", ["Quiz, exam, daily question;", "catalog calculators"], "white")

    k.arrow([(210, 115), (230, 115)])
    k.arrow([(420, 115), (440, 115)])
    k.arrow([(630, 115), (650, 115)])
    k.arrow([(840, 115), (860, 115)])
    k.arrow([(535, 150), (535, 200)])
    k.arrow([(745, 150), (745, 200)])
    k.arrow([(630, 235), (650, 235)])
    k.arrow([(840, 235), (860, 235)])
    k.arrow([(535, 270), (535, 355), (650, 355)])
    k.arrow([(840, 355), (955, 355), (955, 270)])
    k.finish(str(ROOT / "images" / "roadmap.svg"))


def spec_chain() -> None:
    """spec/README.md: the chain from the author's input to the code, and who writes each link."""
    k.begin(1060, 270)
    k.t(20, 26, "The specification, from the author's input to the code", 16, "bold")
    k.legend(20, 40, [("The author's input", "prod"), ("Written together", "guest"),
                      ("Claude decides", "method"), ("Code", "white")])
    w, h = 160, 84
    k.box(20, 100, w, "Author input", ["Answers to questions,", "word for word", "author-input/"], "prod", h=h)
    k.box(210, 100, w, "Brief", ["Goals, scope, principles,", "constraints, assumptions,", "risks, dependencies"], "prod", h=h)
    k.box(400, 100, w, "Requirements", ["What each part must do:", "Why, Source, Given,", "When, Then; scenarios"], "guest", h=h)
    k.box(620, 60, w, "System design", ["How, and why: DESIGN-n", "with rejected options;", "contracts C1 to C5"], "method", h=h)
    k.box(620, 170, w, "Test plan", ["Levels, environments,", "data, criteria,", "traceability"], "guest", h=h)
    k.box(850, 115, 190, "Tests and code", ["In each repository,", "generated from the", "specification"], "white", h=h)
    k.arrow([(180, 142), (210, 142)])
    k.arrow([(370, 142), (400, 142)])
    k.arrow([(560, 125), (590, 125), (590, 102), (620, 102)])
    k.arrow([(560, 160), (590, 160), (590, 212), (620, 212)])
    k.arrow([(780, 102), (815, 102), (815, 140), (850, 140)])
    k.arrow([(780, 212), (815, 212), (815, 175), (850, 175)])
    k.t(20, 255, "tools/spec_check.py checks every link it can read; the brief and the design hold each outcome once, with its reason.", 11.5, "normal", "#555")
    k.finish(str(ROOT / "images" / "spec-chain.svg"))


if __name__ == "__main__":
    system()
    roadmap()
    parts()
    spec_chain()
