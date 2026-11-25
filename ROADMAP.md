# Roadmap

Stage 1 ([SYSTEM.md](SYSTEM.md)). Specification first: M1 settles what is built and how it is tested, before any build milestone starts ([CLAUDE.md](CLAUDE.md), section Specification first). A build milestone's definition of done is its list of requirements, each with its test scenarios in [spec/requirements](spec/requirements). Milestone numbers are names, not order; the order of work is at the end. IDs are explained in the [glossary](spec/glossary.md).

Progress is marked on each line: `[ ]` open, `[x]` done (with the pull request).

## M0 Workspace and checks

- [x] SYSTEM, CONTRACTS, DECISIONS, ROADMAP, OPEN-QUESTIONS and CLAUDE.md in this repository (#1).
- [x] C1 and C3 (the KPI definitions and Agent E2 API contracts) checked in GitHub Actions (#1).
- [x] A tutorial that teaches the method (#2).

## M1 Interview and specification

No code is written in M1.

- [x] Round 1 of the interview answered ([spec/interview-round-1.md](spec/interview-round-1.md)), and its answers moved to DECISIONS W-012 to W-021, [spec/intent.md](spec/intent.md) and the requirements.
- [x] Requirements with test scenarios for every area: 105 requirements, 176 test scenarios (45 on the lab); [tools/spec_check.py](tools/spec_check.py) confirms each has a source and a test.
- [ ] Round 2 answered ([OPEN-QUESTIONS.md](OPEN-QUESTIONS.md)), and the requirements updated.
- [ ] The isvara.io plan reviewed feature by feature ([spec/design/isvara-revamp.md](spec/design/isvara-revamp.md)), and its requirements written.
- [ ] The author approves the requirements of each build milestone before it starts.

## Build milestones

### M2 Contracts tightened and repositories cleaned

- Requirements: R-WS-001 to R-WS-005; R-KPI-001 to R-KPI-007; R-ADP-005 to R-ADP-012.
- Agent E2's plan rewritten for stage 1 and its older benchmarks removed (W-021; Q-58, Q-59), as Agent E2's milestone A1.
- Each child repository runs the cross-repo checks on its pull requests (R-WS-002).
- Depends on: round 2 answers for sections A and C.

### M8 PCM-Adapter's new identity and explicit data states

- Requirements: R-ADP-001 to R-ADP-004; R-ADP-013 to R-ADP-023.
- Depends on: M2; Q-72 to Q-86.

### M9 Lab build for memory tiering

- Requirements: R-LAB-001 to R-LAB-004; R-ADP-024.
- Depends on: the spike of Q-119; M8 for R-ADP-024.

### M10 Agent E2 for stage 1

- Requirements: R-E2-001 to R-E2-019 (Agent E2's milestones A2 to A4).
- Depends on: Q-57, Q-90 to Q-99.

### M3 PCM live demo: one cluster, one KPI

- Requirements: those marked M3 in [spec/requirements/pcm-live.md](spec/requirements/pcm-live.md).
- Depends on: M2; Q-63 to Q-71.

### M4 PCM live demo: the rest

- Requirements: those marked M4 in [spec/requirements/pcm-live.md](spec/requirements/pcm-live.md).
- Depends on: M3, M8, M10.

### M5 isvara.io content from Agent E2

- Requirements: to write from the reviewed [isvara.io plan](spec/design/isvara-revamp.md); R-KPI-008.
- Depends on: the author's replies in the plan; Q-100 to Q-108.

### M6 Agent E2 on isvara.io

- Requirements: to write from the reviewed isvara.io plan; R-E2-015 and R-E2-016.
- Depends on: M5, M10; Q-4 measured.

### M7 isvara.io exam

- Requirements: R-EXAM-001 to R-EXAM-013.
- Depends on: M5; Q-109 to Q-118.

## After isvara.io goes live

- [ ] Keep isvara.io within US$50 a month on Vercel AI Gateway (W-014).
- [ ] The review gate on knowledge files (Q-10).
- [ ] Executable flow steps and the capacity consultation in Agent E2 (Q-62).

## Order of work

1. M1: round 2 and the isvara.io plan review.
2. M2.
3. M8, M9 and M10 in parallel: they touch different repositories.
4. M3, then M4.
5. M5, then M6 and M7.
