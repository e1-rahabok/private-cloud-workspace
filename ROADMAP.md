# Roadmap

The whole plan on one page: where the product is going, what release 1.0 holds, the milestones in order, and what waits for the author. Every line links to its detail. IDs are explained in the [glossary](spec/glossary.md).

## Goal

VMware administrators have the author's knowledge inside their own private cloud, and isvara.io is recognised worldwide as the authority on large-scale private cloud performance and capacity management. The test: a customer gets value without the author ([intent and principles](spec/intent.md)).

## Release 1.0

- **Agent E2:** Day 2 knowledge on Gemma 4 31B, its free-text answers graded automatically, a visible progress state, screenshots and CSV files, sources for every answer ([requirements](spec/requirements/agent-e2-service.md)).
- **VCF vCommunity Adapter:** no value from a partial read, and every KPI definition taken from Agent E2 ([requirements](spec/requirements/pcm-adapter.md), [KPI definitions](spec/requirements/kpi-definitions.md)).
- **PCM:** the synthetic demo unchanged, plus a live demo of the L2 workspace for performance and capacity on the lab ([requirements](spec/requirements/pcm-live.md)).
- **isvara.io:** rebuilt on the three learning paths, with ask, contributions and practice ([plan](spec/design/isvara-plan.md)). This is the main focus on Release 1.0
- **Out of 1.0:** personal dashboards, what-if analysis, the people side of operations, Day 0 and Day 1 knowledge, value management, the VCF vCommunity Adapter's state codes, Agent E2's new knowledge forms ([DECISIONS](DECISIONS.md), WD-026, WD-033, WD-034, WD-035).

![Release 1.0 milestones and what each depends on: M-1 in progress; M0 paused; M1 paused; M2 leads to M5, M3, M4 and M7; M5 to M6; M3 to M6; M4 to M6 and M8; M7 to M8 and M9](images/roadmap.svg)

<details>
<summary>Text of the diagram, for readers that cannot see it</summary>

Colour key: green = Done; orange = In progress; white = Not started or paused.

Boxes, nested as drawn:
- n1 **M0 Workspace** (Not started or paused): Files, checks, tutorial
- n2 **M-1 Claude in SDD mode** (In progress): Rules, gate, hook
- n3 **M5 Live demo: one KPI** (Not started or paused): One cluster, live
- n4 **M6 Live demo: the rest** (Not started or paused): L2 performance, capacity
- n5 **M1 Specification** (Not started or paused): Intent, model, requirements; approval
- n6 **M2 Contracts, clean-up** (Not started or paused): KPI definitions, docs, Agent E2 plan
- n7 **M3 Adapter for live demo** (Not started or paused): Partial reads, key list, settings, accounts
- n8 **M4 Agent E2 for 1.0** (Not started or paused): Grader, progress, files, Day 2 scope
- n9 **M8 isvara.io Ask** (Not started or paused): Agent E2, contributions, protection
- n10 **M7 isvara.io content** (Not started or paused): Paths, articles, search, infographics, tools
- n11 **M9 isvara.io Practice** (Not started or paused): Quiz, mastery map, exam

Arrows (from, to, label):
- n2 M-1 Claude in SDD mode --> n1 M0 Workspace
- n1 M0 Workspace --> n5 M1 Specification
- n5 M1 Specification --> n6 M2 Contracts, clean-up
- n6 M2 Contracts, clean-up --> n3 M5 Live demo: one KPI
- n6 M2 Contracts, clean-up --> n7 M3 Adapter for live demo
- n6 M2 Contracts, clean-up --> n8 M4 Agent E2 for 1.0
- n6 M2 Contracts, clean-up --> n10 M7 isvara.io content
- n3 M5 Live demo: one KPI --> n4 M6 Live demo: the rest
- n7 M3 Adapter for live demo --> n4 M6 Live demo: the rest
- n8 M4 Agent E2 for 1.0 --> n4 M6 Live demo: the rest
- n8 M4 Agent E2 for 1.0 --> n9 M8 isvara.io Ask
- n10 M7 isvara.io content --> n9 M8 isvara.io Ask
- n10 M7 isvara.io content --> n11 M9 isvara.io Practice

Arrows: `-->` solid, `..>` dashed.

</details>

## Milestones

Milestones are numbered in the order of work. The diagram shows which ones can run in parallel. Work happens only in the open milestone: the first one whose heading does not end with "done". A milestone is marked done only after the author approves it. [tools/milestone_gate.py](tools/milestone_gate.py) shows the open milestone and its next item at every prompt, and fails a pull request that changes a file owned only by a later milestone (WD-039). A build milestone is done when every test scenario of its requirements passes ([tools/spec_check.py](tools/spec_check.py) checks that each requirement has one).

### M-1 Claude in SDD mode: in progress

Claude's own rules and the mechanism that holds Claude to them, before any other work (WD-040). Nothing in M-1 is about the product.

- Files in this repository: [`CLAUDE.md`](CLAUDE.md), [`CLAUDE-PROJECT.md`](CLAUDE-PROJECT.md), [`ROADMAP.md`](ROADMAP.md), [`DECISIONS.md`](DECISIONS.md), [`spec/glossary.md`](spec/glossary.md), [`.claude/`](.claude), [`.github/`](.github), [`tools/milestone_gate.py`](tools/milestone_gate.py), [`tools/diagrams.py`](tools/diagrams.py), [`images/roadmap.svg`](images/roadmap.svg).
- [x] One rule for the order of work, its prompt hook and its CI check ([#35](https://github.com/e1-rahabok/private-cloud-workspace/pull/35)).
- [x] CLAUDE.md pruned: one rule per bullet, no rule twice, the method apart from this project's rules ([#36](https://github.com/e1-rahabok/private-cloud-workspace/pull/36)).
- [x] CLAUDE.md holds only the method, for any project; this project's rules, tools and paths are in CLAUDE-PROJECT.md, which CLAUDE.md loads ([#37](https://github.com/e1-rahabok/private-cloud-workspace/pull/37)).
- [ ] The same CLAUDE.md in each child repository, each with its own CLAUDE-PROJECT.md. Done in private-cloud-manager ([#75](https://github.com/e1-rahabok/private-cloud-manager/pull/75)) and isvara ([#2](https://github.com/e1-rahabok/isvara/pull/2)). agent-e2 and PCM-Adapter wait for this session's push access.
- [ ] A check that every copy of CLAUDE.md equals the workspace's.
- [ ] The author approves M-1.

### M0 Workspace, checks and tutorial: paused

Reopened on 2026-11-27: it was marked done without the author's review. Waits for M-1.

- Files in this repository: [`CLAUDE.md`](CLAUDE.md), [`README.md`](README.md), [`ROADMAP.md`](ROADMAP.md), [`DECISIONS.md`](DECISIONS.md), [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md), [`spec/glossary.md`](spec/glossary.md), [`spec/README.md`](spec/README.md), [`spec/requirements/README.md`](spec/requirements/README.md), [`spec/review/`](spec/review), [`.claude/`](.claude), [`.github/`](.github), [`tools/`](tools), [`checks/run_all.py`](checks/run_all.py), [`images/`](images).
- [ ] Each foundation of M0 listed, reviewed with the author one at a time, and approved.
- [x] The workspace files: SYSTEM.md, CONTRACTS.md, DECISIONS.md, ROADMAP.md, OPEN-QUESTIONS.md ([#1](https://github.com/e1-rahabok/private-cloud-workspace/pull/1)).
- [x] The contract checks C1 and C3, run in CI on every pull request and every night ([#1](https://github.com/e1-rahabok/private-cloud-workspace/pull/1)).
- [x] The stop rules and the diagram tool ([#3](https://github.com/e1-rahabok/private-cloud-workspace/pull/3)).
- [x] The writing rules and their check, [tools/style.py](tools/style.py) ([#7](https://github.com/e1-rahabok/private-cloud-workspace/pull/7)).
- [x] The tutorial, first version ([#2](https://github.com/e1-rahabok/private-cloud-workspace/pull/2), [#6](https://github.com/e1-rahabok/private-cloud-workspace/pull/6)). Each session adds its lessons to it afterwards ([CLAUDE-PROJECT.md](CLAUDE-PROJECT.md), section Session end).

### M1 Specification: paused

No code is written in M1. Part of it was written before M-1 and M0 were reopened.

- Files in this repository: [`SYSTEM.md`](SYSTEM.md), [`CONTRACTS.md`](CONTRACTS.md), [`spec/`](spec).

- **Needs the author during M1:** nothing. Claude does the open items below.
- **Needs the author at the end:** one approval of M2, from its [review page](spec/review/M2.md), when every other item is ticked.

- [x] The interview: round 1 answered by the author; round 2 decided or answered ([round 1](spec/interview-round-1.md), [round 2](spec/interview-round-2.md)).
- [x] [Intent and principles](spec/intent.md), the [knowledge model](spec/knowledge-model.md), and the [isvara.io plan](spec/design/isvara-plan.md).
- [x] Requirements with test scenarios, each with its source ([tools/spec_check.py](tools/spec_check.py) prints the totals).
- [ ] Requirements updated for the decisions of 2026-11-26 (WD-024 to WD-027) and the round 2 decisions: [agent-e2-service.md](spec/requirements/agent-e2-service.md), [pcm-live.md](spec/requirements/pcm-live.md), [isvara-exam.md](spec/requirements/isvara-exam.md).
- [ ] isvara.io's requirements written from its plan, in [isvara-content.md](spec/requirements/isvara-content.md) and the files the plan needs.
- [ ] Every requirement file checked against WD-036: a requirement on one repository's own code or files moves to that repository; the workspace keeps the contracts and their checks.
- [x] The milestones renumbered in the order of work, after the lab build left release 1.0 (WD-031).
- [x] The author answered the last questions ([round 3](spec/interview-round-3.md), [round 4](spec/interview-round-4.md), [round 5](spec/interview-round-5.md)). The lab's cluster, datastore and network are asked when the lab build starts, after release 1.0 (WD-031).
- [ ] Last: the author approves the requirements of M2, the first build milestone, from its [review page](spec/review/M2.md).

### M2 Contracts tightened and repositories cleaned

- Files in this repository: [`checks/kpi_definitions.py`](checks/kpi_definitions.py), [`checks/agent_e2_api.py`](checks/agent_e2_api.py).
Requirements as drafted; they may still change in M1. The author approves them at the end of M1, from the [review page](spec/review/M2.md).

- Workspace checks: R-WS-001 to R-WS-007 ([workspace.md](spec/requirements/workspace.md)), including the check that folder and file names carry no version, milestone or status word (WD-030).
- KPI definitions: R-KPI-001 to R-KPI-006 ([kpi-definitions.md](spec/requirements/kpi-definitions.md)): the adapter's tables equal Agent E2's catalog.
- VCF vCommunity Adapter, the parts that follow from the KPI definitions: R-ADP-005 to R-ADP-011 and R-ADP-025 ([pcm-adapter.md](spec/requirements/pcm-adapter.md)).
- Repository clean-up: R-REPO-001 to R-REPO-008 ([repositories.md](spec/requirements/repositories.md)): the adapter's knowledge pages to Agent E2, Agent E2's plan and old benchmarks, the product's name, old repository names, and PCM's folders and files named for what they hold and grouped by workspace.

### M3 VCF vCommunity Adapter for the live demo

- Requirements: R-ADP-018 to R-ADP-023.

### M4 Agent E2 for release 1.0

- Requirements: R-E2-001 to R-E2-020. The grader's answer set holds about 15 questions in release 1.0 (R-E2-004).
- Agent E2 declines Day 0 and Day 1 questions with a pointer to Broadcom's documentation (WD-026).

### M5 Live demo: one cluster, one KPI

- Requirements marked M5 in [pcm-live.md](spec/requirements/pcm-live.md).

### M6 Live demo: the rest

- Requirements marked M6 in [pcm-live.md](spec/requirements/pcm-live.md).

### M7 isvara.io content

- The export from Agent E2 (contract C4), articles on the three learning paths, search, infographics, calculators on the catalog, the weekly summary, the manual ([plan](spec/design/isvara-plan.md)). R-CONTENT-001 ([isvara-content.md](spec/requirements/isvara-content.md)).

### M8 isvara.io Ask and contributions

- Agent E2 on isvara.io in place of AskIO, contributions, and the protection layers (WD-024). R-E2-015, R-E2-016.

### M9 isvara.io Practice

- The quiz and mastery map, the exam (R-EXAM-001 to R-EXAM-013), the daily question, the 2am game's debriefs.

## Order of work

1. M1, to the author's approval of M2.
2. M2.
3. M3 and M4 in parallel: they touch different repositories.
4. M5, then M6.
5. M7, then M8 and M9.

## Waiting for the author

- The licence, before the first customer copies the product (WD-029).
- Approvals at the time of the work: turning on the packet counters (Q-WS-85), the exam's ten questions (Q-WS-113), grading 20 answers once (Q-WS-92).
- Review of each pull request marked as a major change.

## After release 1.0

- Personal dashboards and what-if analysis in PCM; the tenant or application owner role.
- A code review of the VCF vCommunity Adapter: the next page of its [engineering review](https://github.com/e1-rahabok/PCM-Adapter/tree/main/docs/development-guide/engineering-review), after the dated pages of October 2026.
- The people side of operations.
- Agent E2's new knowledge forms: workload footprints, investigations over several steps, "At large scale" notes; then isvara.io's choice of a small or large estate ([knowledge model](spec/knowledge-model.md), section Proposals; WD-035).
- Value management, the fifth pillar of The SP5 Framework: cost, price and business value (WD-034).
- VCF vCommunity Adapter's state codes: every row and KPI says why it has no value (R-ADP-013 to R-ADP-017; WD-033).
- A larger answer set for Agent E2's grader, from about 15 questions toward 40, weighted to the questions visitors ask.
- The lab build for memory tiering: nested ESXi hosts with an NVMe tier (R-LAB-001 to R-LAB-004, R-ADP-024; WD-031). It starts with a spike: can a nested host use a virtual NVMe tier (Q-WS-119)? Claude then asks for the cluster, datastore, network and spare capacity in the lab (Q-WS-120, [round 5](spec/interview-round-5.md)).
- Depth beyond vSphere, grown through contributions: vSAN, NSX, Kubernetes, Guest OS, physical infrastructure.
- Executable flow steps and the capacity consultation in Agent E2.
- An email newsletter for isvara.io's weekly summary.
- Keeping isvara.io within US$50 a month (WD-014).
