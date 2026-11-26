# Roadmap

The whole plan on one page: where the product is going, what release 1.0 holds, the milestones in order, and what waits for the author. Every line links to its detail. IDs are explained in the [glossary](spec/glossary.md).

## Goal

VMware administrators have the author's knowledge inside their own private cloud, and isvara.io is recognised worldwide as the authority on large-scale private cloud performance and capacity management. The test: a customer gets value without the author ([intent and principles](spec/intent.md)).

## Release 1.0

- **Agent E2:** Day 2 knowledge on Gemma 4 31B, its free-text answers graded automatically, a visible progress state, screenshots and CSV files, sources for every answer ([requirements](spec/requirements/agent-e2-service.md)).
- **PCM-Adapter:** a new identity, explicit data states, and every KPI definition taken from Agent E2 ([requirements](spec/requirements/pcm-adapter.md), [KPI definitions](spec/requirements/kpi-definitions.md)).
- **PCM:** the synthetic demo unchanged, plus a live demo of the L2 workspace for performance and capacity on the lab ([requirements](spec/requirements/pcm-live.md)).
- **isvara.io:** rebuilt on the three learning paths, with Ask, contributions and practice ([plan](spec/design/isvara-revamp.md)).
- **Out of 1.0:** personal dashboards, what-if analysis, the people side of operations, Day 0 and Day 1 knowledge ([DECISIONS](DECISIONS.md), W-026).

![Release 1.0 milestones and what each depends on: M0 done; M1 in progress; M2 leads to M3, M8, M10 and M5; M3 to M4; M8 to M9 and M4; M10 to M4 and M6; M5 to M6 and M7](images/roadmap.svg)

<details>
<summary>Text of the diagram, for readers that cannot see it</summary>

Colour key: green = Done; orange = In progress; white = Not started.

Boxes, nested as drawn:
- n1 **M0 Workspace** (Done): Files, checks, tutorial
- n2 **M3 Live demo: one KPI** (Not started): One cluster, live
- n3 **M4 Live demo: the rest** (Not started): L2 performance, capacity
- n4 **M1 Specification** (In progress): Intent, model, requirements; approval
- n5 **M2 Contracts, clean-up** (Not started): KPI definitions, docs, Agent E2 plan
- n6 **M8 Adapter identity** (Not started): New name, data states
- n7 **M9 Lab build** (Not started): Nested hosts with tiering
- n8 **M10 Agent E2 stage 1** (Not started): Grader, progress, files, Day 2 scope
- n9 **M6 isvara.io Ask** (Not started): Agent E2, contributions, protection
- n10 **M5 isvara.io content** (Not started): Paths, articles, search, infographics, tools
- n11 **M7 isvara.io Practice** (Not started): Quiz, mastery map, exam

Arrows (from, to, label):
- n1 M0 Workspace --> n4 M1 Specification
- n4 M1 Specification --> n5 M2 Contracts, clean-up
- n5 M2 Contracts, clean-up --> n2 M3 Live demo: one KPI
- n5 M2 Contracts, clean-up --> n6 M8 Adapter identity
- n5 M2 Contracts, clean-up --> n8 M10 Agent E2 stage 1
- n5 M2 Contracts, clean-up --> n10 M5 isvara.io content
- n2 M3 Live demo: one KPI --> n3 M4 Live demo: the rest
- n6 M8 Adapter identity --> n7 M9 Lab build
- n6 M8 Adapter identity --> n3 M4 Live demo: the rest
- n8 M10 Agent E2 stage 1 --> n3 M4 Live demo: the rest
- n8 M10 Agent E2 stage 1 --> n9 M6 isvara.io Ask
- n10 M5 isvara.io content --> n9 M6 isvara.io Ask
- n10 M5 isvara.io content --> n11 M7 isvara.io Practice

Arrows: `-->` solid, `..>` dashed.

</details>

## Milestones

Milestone numbers are names; the diagram and the order of work give the sequence. A build milestone is done when every test scenario of its requirements passes ([tools/spec_check.py](tools/spec_check.py) checks that each requirement has one).

### M0 Workspace and checks: done

- [x] The workspace files, the contract checks in CI, and the tutorial (#1, #2, #6, #7).

### M1 Specification: in progress

No code is written in M1.

- [x] The interview: round 1 answered by the author; round 2 decided or answered ([round 1](spec/interview-round-1.md), [round 2](spec/interview-round-2.md)).
- [x] [Intent and principles](spec/intent.md), the [knowledge model](spec/knowledge-model.md), and the [isvara.io plan](spec/design/isvara-revamp.md).
- [x] 105 requirements with 176 test scenarios, each with its source.
- [ ] Requirements updated for the decisions of 2026-11-26 (W-024 to W-027) and the round 2 decisions, and isvara.io's requirements written from its plan.
- [x] The author answered the last questions ([round 3](spec/interview-round-3.md)); the lab facts (Q-120, Q-122) come when M9 starts.
- [ ] The author approves the requirements of M2, the first build milestone (listed under M2 below).

### M2 Contracts tightened and repositories cleaned

Requirements, ready for the author's approval:

- Workspace checks: R-WS-001 to R-WS-006 ([workspace.md](spec/requirements/workspace.md)).
- KPI definitions: R-KPI-001 to R-KPI-007 ([kpi-definitions.md](spec/requirements/kpi-definitions.md)).
- PCM-Adapter, the parts that follow from the KPI definitions: R-ADP-005 to R-ADP-012 ([pcm-adapter.md](spec/requirements/pcm-adapter.md)).
- Repository clean-up: R-REPO-001 to R-REPO-006 ([repositories.md](spec/requirements/repositories.md)): the adapter's knowledge pages to Agent E2, Agent E2's plan and old benchmarks, the product's name, old repository names.

### M8 PCM-Adapter's new identity and data states

- Requirements: R-ADP-001 to R-ADP-004; R-ADP-013 to R-ADP-023.

### M9 Lab build for memory tiering

- Requirements: R-LAB-001 to R-LAB-004; R-ADP-024. Starts with a spike: can a nested host use a virtual NVMe tier (Q-119)?

### M10 Agent E2 for stage 1

- Requirements: R-E2-001 to R-E2-019.
- The knowledge model's proposals in agent-e2: a configuration pillar tag, workload footprints, investigations over several steps, "At large scale" notes ([knowledge model](spec/knowledge-model.md), section Proposals).
- Agent E2 declines Day 0 and Day 1 questions with a pointer to Broadcom's documentation (W-026).

### M3 Live demo: one cluster, one KPI

- Requirements marked M3 in [pcm-live.md](spec/requirements/pcm-live.md).

### M4 Live demo: the rest

- Requirements marked M4 in [pcm-live.md](spec/requirements/pcm-live.md).

### M5 isvara.io content

- The export from Agent E2 (contract C4), articles on the three learning paths, search, infographics, calculators on the catalog, the weekly summary, the manual ([plan](spec/design/isvara-revamp.md)). R-KPI-008.

### M6 isvara.io Ask and contributions

- Agent E2 on isvara.io in place of AskIO, contributions, and the protection layers (W-024). R-E2-015, R-E2-016.

### M7 isvara.io Practice

- The quiz and mastery map, the exam (R-EXAM-001 to R-EXAM-013), the daily question, the 2am game's debriefs.

## Order of work

1. M1, to the author's approval of M2.
2. M2.
3. M8, M9 and M10 in parallel: they touch different repositories.
4. M3, then M4.
5. M5, then M6 and M7.

## Waiting for the author

- The lab facts for M9 ([OPEN-QUESTIONS.md](OPEN-QUESTIONS.md), Q-120 and Q-122): Claude asks when M9 starts.
- The licence, before the first customer copies the product (W-029).
- Approvals at the time of the work: removing the old pack from the lab (Q-79), turning on the packet counters (Q-85), the exam's ten questions (Q-113), grading 20 answers once (Q-92).
- Review of each pull request marked as a major change.

## After release 1.0

- Personal dashboards and what-if analysis in PCM; the tenant or application owner role.
- The people side of operations.
- Depth beyond vSphere, grown through contributions: vSAN, NSX, Kubernetes, Guest OS, physical infrastructure.
- Executable flow steps and the capacity consultation in Agent E2.
- An email newsletter for isvara.io's weekly summary.
- Keeping isvara.io within US$50 a month (W-014).
