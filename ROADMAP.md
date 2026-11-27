# Roadmap

The whole plan on one page: where the product is going, what release 1.0 holds, the milestones in order, and what waits for the author. Every line links to its detail. IDs are explained in the [glossary](spec/glossary.md).

## Goal

VMware administrators have the author's knowledge inside their own private cloud, and isvara.io is recognised worldwide as the authority on large-scale private cloud performance and capacity management. The test: a customer gets value without the author ([intent and principles](spec/intent.md)).

## Release 1.0

Two goals, and the work that supports them:

- **isvara.io, the main goal and most of the work:** rebuilt on the three learning paths, with articles, Ask Agent E2, contributions and practice ([plan](spec/design/isvara-plan.md)).
- **PCM's live demo, the second goal:** the synthetic demo unchanged, plus a live demo of the L2 workspace for performance and capacity on the lab ([requirements](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/requirements/live-demo.md)).
- **Agent E2, in support of both:** Day 2 knowledge on Gemma 4 31B, its free-text answers graded automatically, a visible progress state, screenshots and CSV files, sources for every answer ([requirements](https://github.com/e1-rahabok/agent-e2/blob/main/project/requirements/answer-service.md), [API](spec/requirements/agent-e2-api.md)).
- **VCF vCommunity Adapter, in support of the live demo:** no value from a partial read, and every KPI definition taken from Agent E2 ([requirements](https://github.com/e1-rahabok/PCM-Adapter/blob/main/spec/requirements/adapter.md), [KPI definitions](spec/requirements/kpi-definitions.md)).
- **Out of 1.0:** personal dashboards, what-if analysis, the people side of operations, Day 0 and Day 1 knowledge, value management, the VCF vCommunity Adapter's state codes, Agent E2's new knowledge forms ([DECISIONS](DECISIONS.md), WD-026, WD-033, WD-034, WD-035).

![Release 1.0 milestones and what each depends on: Claude's method done before them; M1 in progress; M2 to M8 not started; M1 leads to M2; M2 to M3 and M4; M3 to M5 and M8; M4 to M5 and M6; M5 and M6 to M7](images/roadmap.svg)

<details>
<summary>Text of the diagram, for readers that cannot see it</summary>

Colour key: green = Done; orange = In progress; white = Not started.

Boxes, nested as drawn:
- n1 **Claude's method** (Done): Rules, gate, hook; done before the milestones
- n2 **M1 Release 1.0 specified** (In progress): Every requirement, isvara.io design; no code
- n3 **M2 Contracts, clean-up** (Not started): Checks in every repository; names, PCM folders
- n4 **M3 Agent E2 for both** (Not started): Jobs, files, sources, grader, Day 2 only
- n5 **M8 PCM live demo** (Not started): Adapter fixes, live L2; every lab test
- n6 **M4 isvara.io reading** (Not started): Export, articles, paths, search, infographics
- n7 **M5 isvara.io Ask** (Not started): Agent E2, contributions, protection
- n8 **M7 isvara.io switch-over** (Not started): Home, What's New, manual; old links redirected
- n9 **M6 isvara.io practice** (Not started): Quiz, exam, daily question; catalog calculators

Arrows (from, to, label):
- n1 Claude's method --> n2 M1 Release 1.0 specified
- n2 M1 Release 1.0 specified --> n3 M2 Contracts, clean-up
- n3 M2 Contracts, clean-up --> n4 M3 Agent E2 for both
- n4 M3 Agent E2 for both --> n5 M8 PCM live demo
- n3 M2 Contracts, clean-up --> n6 M4 isvara.io reading
- n4 M3 Agent E2 for both --> n7 M5 isvara.io Ask
- n6 M4 isvara.io reading --> n7 M5 isvara.io Ask
- n7 M5 isvara.io Ask --> n8 M7 isvara.io switch-over
- n6 M4 isvara.io reading --> n9 M6 isvara.io practice
- n9 M6 isvara.io practice --> n8 M7 isvara.io switch-over

Arrows: `-->` solid, `..>` dashed.

</details>

## Rules of the milestones

- The milestones are numbered from M1 in the order of work (WD-042). One is open at a time: the first whose heading does not end with ": done" (WD-039).
- [tools/milestone_gate.py](tools/milestone_gate.py) shows the open milestone and its next item at every prompt. It fails a pull request that changes a file owned only by a later milestone, and fails when two milestones own one file or the numbers do not run M1, M2, M3 in order.
- Each requirement belongs to exactly one milestone, or to the list after release 1.0. [tools/milestone_review.py](tools/milestone_review.py) fails otherwise, and writes one review page per milestone from the requirement files.
- A build milestone is done when every test scenario of its requirements passes ([tools/spec_check.py](tools/spec_check.py) checks that each requirement has one). Every test scenario that needs the lab sits in M8, the only milestone that uses the lab.
- The author approves each milestone. For M1 only, the author delegated the approval to Claude's self-review, and reviews M1 afterwards (WD-042).

## Done before the milestones

Claude's working method, about how Claude works and never about the product (WD-040), approved by the author on 2026-11-27:

- One rule for the order of work, its prompt hook and its CI check ([#35](https://github.com/e1-rahabok/private-cloud-workspace/pull/35)).
- CLAUDE.md pruned: one rule per bullet, no rule twice, the method apart from this project's rules ([#36](https://github.com/e1-rahabok/private-cloud-workspace/pull/36)).
- CLAUDE.md holds only the method, for any project; this project's rules, tools and paths are in CLAUDE-PROJECT.md, which CLAUDE.md loads ([#37](https://github.com/e1-rahabok/private-cloud-workspace/pull/37)).
- The same CLAUDE.md in each child repository, each with its own CLAUDE-PROJECT.md: agent-e2 ([#475](https://github.com/e1-rahabok/agent-e2/pull/475)), PCM-Adapter ([#105](https://github.com/e1-rahabok/PCM-Adapter/pull/105)), private-cloud-manager ([#75](https://github.com/e1-rahabok/private-cloud-manager/pull/75)), isvara ([#2](https://github.com/e1-rahabok/isvara/pull/2)).
- A check that every copy of CLAUDE.md equals the workspace's, [tools/claude_md_copies.py](tools/claude_md_copies.py), run in CI for all but isvara ([#39](https://github.com/e1-rahabok/private-cloud-workspace/pull/39)).
- The workspace files, the contract checks C1 and C3, the stop rules, the diagram tool, the writing rules and their check, and the tutorial's first version ([#1](https://github.com/e1-rahabok/private-cloud-workspace/pull/1), [#2](https://github.com/e1-rahabok/private-cloud-workspace/pull/2), [#3](https://github.com/e1-rahabok/private-cloud-workspace/pull/3), [#6](https://github.com/e1-rahabok/private-cloud-workspace/pull/6), [#7](https://github.com/e1-rahabok/private-cloud-workspace/pull/7)). M1 reviews them against the decisions.

## Milestones

### M1 Release 1.0 specified: in progress

- **Outcome:** every requirement of release 1.0 is written, testable, free of contradictions and kept in the repository that implements it, and every later milestone has its review page. No code is written in M1.
- **Runs:** in a cloud session; documents only.
- **The author:** delegated the approval to Claude's self-review (WD-042); reviews M1 on return and can reopen it.
- Files in this repository: [`ROADMAP.md`](ROADMAP.md), [`DECISIONS.md`](DECISIONS.md), [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md), [`README.md`](README.md), [`SYSTEM.md`](SYSTEM.md), [`CONTRACTS.md`](CONTRACTS.md), [`spec/`](spec), [`images/`](images), [`tools/milestone_gate.py`](tools/milestone_gate.py), [`tools/milestone_review.py`](tools/milestone_review.py), [`tools/spec_check.py`](tools/spec_check.py), [`tools/diagrams.py`](tools/diagrams.py), [`tools/docs.py`](tools/docs.py), [`tools/requirement_files.py`](tools/requirement_files.py), [`.github/`](.github).

- [x] The milestones revamped: M1 to M8, one outcome each, no file or requirement in two milestones, both checked by code (WD-042) ([#40](https://github.com/e1-rahabok/private-cloud-workspace/pull/40), [agent-e2#476](https://github.com/e1-rahabok/agent-e2/pull/476)).
- [x] The foundations reviewed against the decisions: SYSTEM.md, CONTRACTS.md, README.md, the glossary and the tutorial's method chapters ([#41](https://github.com/e1-rahabok/private-cloud-workspace/pull/41)).
- [ ] Every requirement in the repository that implements it (WD-036); the workspace keeps the contracts and their checks, and its tools read the requirements of every repository.
- [ ] Every contradiction between two requirement files fixed, each listed in its pull request.
- [ ] Agent E2's requirements updated for the Day 2 scope (WD-026) and the round 2 decisions; the parts that need live lab facts moved to M8.
- [ ] Requirements on the callers of Agent E2 moved to the callers: PCM's to M8, isvara.io's to M5.
- [ ] The live demo's requirements updated for the round 2 decisions.
- [ ] Every test scenario that needs the lab in M8; M2 and M3 keep the scenarios that run anywhere.
- [ ] The exam's requirements updated for the round 2 decisions.
- [ ] isvara.io before and after: one document, feature by feature, for the author's review before anything is built (answer to Q-WS-41).
- [ ] isvara.io's requirements for M4 to M7, written from that document.
- [ ] A fresh agent reads the specification cold and finds no contradiction, no requirement that cannot be tested, and no requirement outside a milestone.
- [ ] Approval: Claude's self-review, delegated by the author (WD-042).

### M2 Contracts checked and repositories cleaned

- **Outcome:** every contract that exists today is checked on every pull request of every repository, and each repository has the names and the folder layout the decisions set.
- **Needs:** M1.
- **Runs:** in a cloud session. The adapter's lab scenarios run in M8.
- Files in this repository: [`checks/`](checks), [`tools/style.py`](tools/style.py).
- **Requirements:** R-WS-001 to R-WS-007 and R-REPO-006 ([workspace.md](spec/requirements/workspace.md)), R-KPI-001 to R-KPI-006 ([kpi-definitions.md](spec/requirements/kpi-definitions.md)), R-ADP-005 to R-ADP-011 and R-ADP-025 ([adapter.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/spec/requirements/adapter.md)), R-REPO-001 and R-REPO-002 (PCM-Adapter's [clean-up.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/spec/requirements/clean-up.md)), R-REPO-003 and R-REPO-004 (agent-e2's [clean-up.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/requirements/clean-up.md)), R-REPO-005, R-REPO-007 and R-REPO-008 (private-cloud-manager's [clean-up.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/requirements/clean-up.md)).

### M3 Agent E2 serves PCM and isvara.io

- **Outcome:** one Agent E2 service answers both callers: long answers as jobs with a visible stage, screenshots and CSV files, sources by ID and title, time and tokens per answer, Day 2 questions only; its free-text answers are graded automatically.
- **Needs:** M2, so the contract check C3 (the Agent E2 API) runs on every pull request.
- **Runs:** in a cloud session. The graded runs need the Vercel AI Gateway key, within US$100 a run (WD-014). The author grades 20 answers once (Q-WS-92).
- **Requirements:** R-E2-001 to R-E2-019 (agent-e2's [answer-service.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/requirements/answer-service.md); R-E2-009, R-E2-017 and R-E2-019 in the workspace's [agent-e2-api.md](spec/requirements/agent-e2-api.md)).

### M4 isvara.io reading

- **Outcome:** on the Vercel preview, a visitor reads every Agent E2 knowledge file as an article, finds it through the three learning paths and through search, and sees the first infographics. isvara.io holds no knowledge of its own.
- **Needs:** M1 for the design, M2 for the checks. It does not need M3.
- **Runs:** in a cloud session. The rewrite of each article and its checks need the Vercel AI Gateway key.
- **Requirements:** the export from Agent E2 (contract C4, knowledge content for isvara.io), articles, paths, search and infographics, written in M1.

### M5 isvara.io Ask and contributions

- **Outcome:** on the preview, a visitor asks Agent E2 a question, with screenshots and CSV files, follows its progress and opens its sources; sends a contribution to a private queue; and the protection layers stop floods, bots, unsafe files and hidden instructions.
- **Needs:** M3 for the Agent E2 API, M4 for the articles that sources open.
- **Runs:** in a cloud session. Where the public Agent E2 runs is chosen after measuring (Q-WS-4); a new hosting account would need the author.
- **Requirements:** Ask, contributions and protection, written in M1.

### M6 isvara.io practice and tools

- **Outcome:** the quiz with its mastery map, the exam, the daily question and the 2am game's debriefs link to articles; the calculators and the RVTools health check take every number from Agent E2's catalog; the dropped tools are gone.
- **Needs:** M4 for the articles.
- **Runs:** in a cloud session. The author approves the exam's ten questions once (Q-WS-113).
- **Requirements:** R-EXAM-001 to R-EXAM-013 (isvara's [exam.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/exam.md)), R-CONTENT-001 (isvara's [content.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/content.md)), and the quiz, mastery map, daily question and calculators, written in M1.

### M7 isvara.io switched over

- **Outcome:** isvara.io serves the rebuilt site: the home page, What's New with its weekly summary, the manual for copying the product privately, downloads and the MCP endpoint on Agent E2; every old address redirects to the page that covers it.
- **Needs:** M4, M5 and M6.
- **Runs:** in a cloud session. The author approves the switch from the preview.
- **Requirements:** home page, What's New, manual, downloads, MCP endpoint, redirects and the switch-over, written in M1.

### M8 PCM live demo

- **Outcome:** PCM's live demo shows the lab's L2 workspace for performance and capacity, read from VCF Operations; the VCF vCommunity Adapter publishes no value built from a partial read; Agent E2 explains a real lab KPI correctly; and every test scenario of release 1.0 that needs the lab has run.
- **Needs:** M2 for the catalog names, M3 for Agent E2's jobs and facts.
- **Runs:** in the lab, from the author's laptop over the VPN, with the adapter's build, install, restart and validation tools. A cloud session writes the code and the tests that run anywhere.
- **First slice:** one lab cluster's Cluster Performance on the L2 Performance tab (R-LIVE-001, R-LIVE-024, R-LIVE-030), then the rest.
- **Requirements:** R-ADP-018 to R-ADP-023 ([adapter.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/spec/requirements/adapter.md)), R-LIVE-001 to R-LIVE-032 and R-E2-020 (private-cloud-manager's [live-demo.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/requirements/live-demo.md)); the check of contract C2 (KPI metric keys).
- **Release 1.0 is done** when the author approves M8.

## Waiting for the author

- The licence, before the first customer copies the product (WD-029).
- Approval of each milestone from M2 on.
- At M3: the Vercel AI Gateway key for this cloud environment, and grading 20 answers once (Q-WS-92).
- At M6: the exam's ten questions (Q-WS-113).
- At M7: the switch from the preview.
- At M8: a lab session with the laptop and the VPN, and turning on the packet counters in the lab policy (Q-WS-85).
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
