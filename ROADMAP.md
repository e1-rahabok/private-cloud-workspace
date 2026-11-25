# Roadmap

Stage 1 ([SYSTEM.md](SYSTEM.md)). Specification first: M1 settles what is built and how it is tested, before any build milestone starts. Each build milestone is a thin slice across the repositories. Its definition of done is the list of requirement IDs it delivers, each with its test scenarios in [`spec/requirements/`](spec/requirements).

Progress is marked on each line: `[ ]` open, `[x]` done (with the pull request).

## M0 Workspace and checks

- [x] SYSTEM, CONTRACTS, DECISIONS, ROADMAP, OPEN-QUESTIONS and CLAUDE.md in this repository (#1).
- [x] C1 and C3 run in GitHub Actions on push, pull request, daily and on demand, and pass (#1).
- [x] A tutorial that teaches the method, with this workspace as the case study (#2).

## M1 Interview and specification

No code is written in M1. Done when:

- [ ] Every question in [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) has an answer from the author, and each answer is moved to DECISIONS or a requirement.
- [ ] [`spec/intent.md`](spec/intent.md) states, for the product and for each app, who it is for, what success looks like, and what is not done. The author has approved it.
- [ ] Each build milestone below has its requirements in [`spec/requirements/`](spec/requirements): one ID each, written as Given, When, Then, with the answer or decision it comes from.
- [ ] Each requirement has at least one test scenario: the data, the steps, the expected result, and where it runs (anywhere, or the lab).
- [ ] Each test scenario names the test or check that will automate it, or says why it stays manual.
- [ ] A check confirms the links: every requirement has a test scenario, and every scenario names an existing requirement.
- [ ] The author has approved the requirements and scenarios of the next build milestone.

## Build milestones

The lines below are the scope of each milestone as known today. M1 replaces each list with requirement IDs.

### M2 Close the known gaps

- C1 runs with an empty `NAME_GAPS` (Q-1).
- C1 also checks the part names PCM uses, from a structured list in PCM's specification.
- No file outside an archive names the old repository VCF-vCommunity-Adapter.
- Each child repository runs [`checks/run_all.py`](checks/run_all.py) on its own pull requests.

### M3 Live VCF Operations in PCM: one cluster, one KPI

- A "Live VCF Operations" choice in the demo control; Synthetic ACME stays the default.
- One lab cluster's Cluster Performance for the last 24 hours, read from VCF Operations, matching it within rounding.
- Missing or failed data shows as no data or stale, never as zero or green.
- PCM lists every key it reads; C2 checks them against PCM-Adapter.

### M4 Live VCF Operations: the rest of release 1.0

- The other KPIs and objects on the release 1.0 pages, by the same pattern as M3.
- C2 also runs against the lab.

### M5 isvara.io content from Agent E2: one pilot page

- One concept page generated from the Agent E2 knowledge base, with no hand edits.
- The export is a written contract (C4) with a check.

### M6 Agent E2 on isvara.io

- Agent E2 answers on isvara.io in place of AskIO, through the C3 contract.
- isvara.io's eval and injection batteries pass against Agent E2.

### M7 isvara.io exam

- 10 short, very hard questions for people, with the reasoning shown after each answer (W-006).
