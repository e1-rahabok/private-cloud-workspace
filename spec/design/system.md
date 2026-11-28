# System design

How the parts of release 1.0 are built and why: where each part runs, how data flows, the contracts between the repositories, the qualities the system must have, and the design choices that deliver them. Claude owns this design. The [brief](../brief.md) holds the author's input that bounds it, and the [requirements](../requirements) say what each part must do. A design inside one repository stays in that repository: Agent E2's [ARCHITECTURE.md](https://github.com/e1-rahabok/agent-e2/blob/main/ARCHITECTURE.md), PCM's design notes under [`pcm/`](https://github.com/e1-rahabok/private-cloud-manager/tree/main/pcm), the adapter's [development guide](https://github.com/e1-rahabok/PCM-Adapter/tree/main/docs/development-guide) and isvara's [CLAUDE-PROJECT.md](https://github.com/e1-rahabok/isvara/blob/main/CLAUDE-PROJECT.md). IDs are explained in the [glossary](../glossary.md).

## Two web apps, one knowledge service

![The system in release 1.0: PCM, Agent E2, VCF Operations with the VCF vCommunity Adapter in the lab; isvara.io, its planned Agent E2 and the model gateway on the Internet; the contracts C1 to C5 between them](../../images/system.svg)

<details>
<summary>Text of the diagram, for readers that cannot see it</summary>

Colour key: grey = PCM; blue = Agent E2; green = VCF vCommunity Adapter; purple = isvara.io; orange = Model.

Boxes, nested as drawn:
- n1 **PCM** (PCM): Web app for operations roles; synthetic ACME or live data; lab VM, https://10.114.1.29
- n2 **Agent E2 for PCM** (Agent E2): Knowledge service over HTTP; owns all domain knowledge; same lab VM, port 8090
- n3 **isvara.io** (isvara.io): Public learning site; on Vercel; no live system
- n4 **Agent E2 for isvara.io** (Agent E2): Where it runs: measured and chosen in M5 (Q-WS-4)
- n5 **VCF Operations**: Lab, https://10.115.1.81
  - n6 **VCF vCommunity Adapter** (VCF vCommunity Adapter): Computes the KPIs inside VCF Operations, under vCommunity|
- n7 **Vercel AI Gateway** (Model): Cloud model for release 1.0

Arrows (from, to, label):
- n1 PCM --> n2 Agent E2 for PCM: C3
- n1 PCM --> n5 VCF Operations: C2 Suite API, scenario 7
- n2 Agent E2 for PCM ..> n6 VCF vCommunity Adapter: C1 KPI definitions
- n2 Agent E2 for PCM --> n7 Vercel AI Gateway: C5
- n2 Agent E2 for PCM ..> n3 isvara.io: C4
- n3 isvara.io ..> n4 Agent E2 for isvara.io: C3
- n4 Agent E2 for isvara.io ..> n7 Vercel AI Gateway: C5

Notes on the diagram:
- Dashed: planned

Arrows: `-->` solid, `..>` dashed.

</details>

| Part | Repository | Runs where | Talks to |
|---|---|---|---|
| PCM | private-cloud-manager | Lab Linux VM moltbot29, https://10.114.1.29 (VPN) | Agent E2 over HTTP; VCF Operations Suite API (scenario 7) |
| Agent E2 for PCM | agent-e2 | Same lab VM, port 8090, as a systemd service | Vercel AI Gateway |
| VCF vCommunity Adapter | PCM-Adapter | Inside the lab VCF Operations, https://10.115.1.81 (VPN) | vCenter, VCF Operations |
| isvara.io | isvara | Vercel, public | Agent E2 (planned, ROADMAP M5); today its own AskIO agent |
| Agent E2 for isvara.io | agent-e2 | Chosen in ROADMAP M5 after measuring start-up time and cost per answer (Q-WS-4) | Vercel AI Gateway |


## Sources of each kind of data

| Thing | Source | Used by |
|---|---|---|
| KPI definitions: names, parts, limits, bands | Agent E2's [catalog](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge/catalog) | VCF vCommunity Adapter, PCM, Agent E2 |
| KPI values | VCF vCommunity Adapter, published in VCF Operations under `vCommunity\|` | PCM scenario 7, through the Suite API |
| Synthetic values | PCM's generator, [`pcm/core/generator.py`](https://github.com/e1-rahabok/private-cloud-manager/blob/main/pcm/core/generator.py) | PCM scenarios 1 to 6 |
| Explanations and answers | Agent E2 | PCM's Agent E2 panel; isvara.io (planned) |
| Reading content | Today: the Word books. Planned: the Agent E2 knowledge base | isvara.io |

## PCM demo scenarios

PCM is a web application that runs in a browser. In release 1.0 all of PCM is a demo. The demo control at the top of every page lists the demo scenarios, one per role:

1. CIO
2. NOC wall
3. NOC L1 engineer
4. L2 platform engineer
5. Capacity planner
6. Docs reader (auditor)

- **Scenarios 1 to 6** show synthetic data: ACME, a global bank with stories written relative to now. They show Agent E2 at its best.
- **Scenario 7, added in release 1.0** (ROADMAP M8): the L2 platform engineer on the author's lab VCF Operations, with live data. It proves PCM reads real data. It is still a demo, and the lab is too quiet to show Agent E2 well.

## PCM and the VCF vCommunity Adapter

The VCF vCommunity Adapter is the management pack installed inside VCF Operations. Its repository is [PCM-Adapter](https://github.com/e1-rahabok/PCM-Adapter). How PCM and the adapter relate, by mechanism:

- **Code:** separate repositories, built and installed separately. Neither contains code of the other.
- **Network:** PCM never connects to the adapter. PCM calls the VCF Operations Suite API, and the adapter is invisible to PCM.
- **Data:** the adapter computes KPIs and stores them in VCF Operations. Scenario 7 reads them there.
- **Dependency:** scenario 7 shows no KPI data without the adapter installed. Scenarios 1 to 6 do not need it.
- **Contract:** [C2, KPI metric keys](#contracts), the keys the adapter publishes and PCM reads.

Describe this relation by one of these mechanisms. "Part of PCM" means the data dependency: PCM's live KPIs come from the adapter.

## Lab

| Host | What | Access |
|---|---|---|
| 10.114.1.29 (moltbot29) | PCM and Agent E2 | VPN from the author's laptop. Secrets in `/etc/pcm/pcm.env` on the VM |
| 10.115.1.81 | VCF Operations 9 with the VCF vCommunity Adapter installed | VPN. Laptop credentials: `$HOME\.secrets\vcf-ops-readonly.xml` and `vcf-ops-admin.xml` (DESIGN-9; Q-WS-84) |
| 10.115.1.87 | vCenter | VPN. Laptop credential: `$HOME\.secrets\vcenter-10.115.1.87.xml` |

## Contracts

Every interface between two repositories. Each has one owner, its consumers, where its shape is written, and the check that proves both sides still agree (DESIGN-5). The IDs C1 to C5 are also in the [glossary](../glossary.md); the requirements per contract are in [requirements](../requirements).

| ID | Contract                     | Owner, then consumers              | Check                                                             |
| -- | ---------------------------- | ---------------------------------- | ----------------------------------------------------------------- |
| C1 | KPI definitions              | agent-e2; VCF vCommunity Adapter, PCM, isvara | [`checks/kpi_definitions.py`](../../checks/kpi_definitions.py), running |
| C2 | KPI metric keys              | VCF vCommunity Adapter; PCM (live demo)       | Planned in ROADMAP M8, the PCM live demo                          |
| C3 | Agent E2 API                 | agent-e2; PCM, isvara (planned)    | [`checks/agent_e2_api.py`](../../checks/agent_e2_api.py), running       |
| C4 | Knowledge content for isvara | agent-e2; isvara                   | `checks/knowledge_export.py`, planned in ROADMAP M4          |
| C5 | Model gateway                | Vercel AI Gateway; agent-e2        | `checks/model_gateway.py`, planned in ROADMAP M3                  |

### C1 KPI definitions

- **Owner:** agent-e2, [`knowledge/catalog/thresholds-performance.yaml`](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) (section `kpi`), `thresholds-risk.yaml` and `thresholds-capacity.yaml` (section `model`). One row per sub-metric: name with unit, group, direction, five limits per interval, `excluded_when_green`.
- **Implementer:** VCF vCommunity Adapter, `Management Pack/app/metrics/`: one module per KPI, a `METRICS` table of `Metric` rows (name, unit, five limits, `skip_when_green`) and a `LABELS` table that gives a row its catalog name.
- **Consumer:** PCM shows the parts under the catalog names (PCM's decisions D-113 and D-115 in [decisions.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md)) in [`pcm/l2/spec/catalog.yaml`](https://github.com/e1-rahabok/private-cloud-manager/blob/main/pcm/l2/spec/catalog.yaml). PCM's live demo finds each part's catalog name by its key ([R-LIVE-018](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/requirements/live-demo.md)), checked in ROADMAP M8; the synthetic demo's names in prose are not checked in release 1.0.
- **The check** matches each sub-metric by key (the catalog row's `key` against the name the adapter's KPI module gives the row), then compares the name (the adapter's label against the catalog name without its unit), the five limits, excluded-when-green and the interval, for Cluster Performance, ESXi Performance, VM Performance, Guest OS Performance, Cluster Risk and Cluster Consumption. It also compares the band table and the closure levels of the adapter's Periodic Cluster Check with the catalog's score lines and Close for Business decisions. [`checks/test_kpi_definitions.py`](../../checks/test_kpi_definitions.py) plants a break of each kind and expects the check to fail.
- **To change a KPI:** change Agent E2's knowledge file and catalog first, then the VCF vCommunity Adapter, in the same session, with the check run before both merges.
- **Status:** names, limits, excluded-when-green and intervals agree for every sub-metric, and the score bands and the closure levels agree with the adapter's Periodic Cluster Check. The adapter's one Cluster Risk level is compared with the catalog's production row, which release 1.0 applies to every cluster (DESIGN-18). [`checks/run_all.py`](../../checks/run_all.py) prints the counts.

### C2 KPI metric keys

- **Owner:** the VCF vCommunity Adapter (repository PCM-Adapter). Keys are `vCommunity|<KPI>|<sub-metric or score>`, for example `vCommunity|Cluster Performance|Cluster Performance Score`, on the vCenter objects in VCF Operations.
- **Consumer:** PCM's demo scenario 7 (live) reads them through the VCF Operations Suite API (PCM D-064, D-096). PCM never connects to the adapter itself; without the adapter installed, scenario 7 has no KPI data.
- **Check, ROADMAP M8:** PCM lists every key it reads in one structured file; the check confirms each key is one the adapter publishes, and, against the lab, that it has data.
- **Status:** no PCM connector yet.

### C3 Agent E2 API

- **Owner:** agent-e2, [`harness/answer_service.py`](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py) (its docstring is the specification). Endpoints: `POST /v1/answer`, `POST /v1/topic`, `POST /v1/suggest` (page and card), `GET /v1/health`.
- **Consumer:** PCM, [`pcm/core/agent_e2.py`](https://github.com/e1-rahabok/private-cloud-manager/blob/main/pcm/core/agent_e2.py), generated from [`pcm/core/spec/catalog/settings.yaml`](https://github.com/e1-rahabok/private-cloud-manager/blob/main/pcm/core/spec/catalog/settings.yaml) and [`pcm/l2/spec/pages/frame.md`](https://github.com/e1-rahabok/private-cloud-manager/blob/main/pcm/l2/spec/pages/frame.md).
- **The check** starts the real service in mock mode (no model, no network) and calls it with PCM's own client code. It checks every field PCM reads, by name and type, on the raw responses: PCM's client turns errors into `source: unavailable`, which would hide a broken contract.
- **Status:** running; [`checks/run_all.py`](../../checks/run_all.py) prints the endpoints and the differences.

### C4 Knowledge content for isvara

- Agent E2's knowledge base becomes the source of isvara.io's reading pages, replacing the Word books (DESIGN-3). Its structure is built for a model to read, so the shape of the export is design work (ROADMAP M1), built in ROADMAP M4.
- **Shape:** one schema in this workspace, `checks/knowledge_export_schema.json`, that agent-e2's export and isvara.io's build both check against ([knowledge-export.md](../requirements/knowledge-export.md)).
- **Status:** not built; planned in ROADMAP M4.

### C5 Model gateway

- **Owner:** Vercel AI Gateway, an OpenAI-compatible service; Agent E2 calls it with the key `AI_GATEWAY_API_KEY`.
- **Check, ROADMAP M3:** one call to the model agent-e2 is set to, with the gateway key; without the key it reports not run ([R-WS-008](../requirements/workspace.md)). It is a third-party API, so the check proves only that the configured model answers.
- **Status:** not built.

### Changing a contract

1. **Expand:** the owner adds the new shape and keeps the old one working.
2. **Migrate:** each consumer moves to the new shape, one pull request per repository.
3. **Contract:** the owner removes the old shape.

The checks pass after every step. A pull request that breaks a check is not merged.

## Quality attributes

What each quality means for release 1.0, a demo in the lab and a public site, and the design choices below that deliver it.

| Quality | Release 1.0 target | Choices |
|---|---|---|
| Correctness | No confident wrong answer; no value built from a partial read | DESIGN-17, DESIGN-18, DESIGN-19 |
| Security and privacy | Secrets outside the repositories; public input treated as data; little data kept | DESIGN-9 to DESIGN-13 |
| Performance | A live page in under 5 seconds; progress on an answer every 10 seconds | DESIGN-14, DESIGN-15 |
| Scalability | Public traffic absorbed by Vercel; answer jobs on one long-running process | DESIGN-12, DESIGN-16 |
| Availability | A demo on one lab VM, no redundancy; a failure shows as "No data" | DESIGN-15, DESIGN-17 |
| Maintainability | One master per fact; every contract checked; guessable names; traced input | DESIGN-2 to DESIGN-8 |
| Cost | US$100 a benchmark run; US$50 a month for isvara.io | DESIGN-16, DESIGN-20 |
| Portability | Copied privately; nothing depends on the author's services at run time | DESIGN-1, DESIGN-4 |

## Design choices

Each choice is Claude's, made from the [brief](../brief.md) and the requirements. It states the choice, why, the options rejected and why, and the brief items and requirements it serves. A choice inside one repository stays in that repository's design notes; this file holds the choices that span repositories or set a quality for the whole system. A changed choice is edited in place; git keeps the history.

### Architecture

- **DESIGN-1 One knowledge service for two web apps.** PCM, private and in the lab, and isvara.io, public on Vercel, are two web apps. Both call Agent E2 over HTTP for every answer (contract C3), and Agent E2 calls its model through Vercel AI Gateway (C5). Agent E2 runs twice: on the lab VM for PCM, and as a public service for isvara.io. isvara.io connects to no live system. Agent E2 replaces AskIO on isvara.io.
  - Why: both apps give the same answer from the same knowledge (PRINCIPLE-5), and a fix to Agent E2 reaches both.
  - Rejected: (a) keep AskIO on isvara.io, which loads the books into its prompt: two answer engines drift apart, and the books would stay a second master. (b) One Agent E2 for both apps: the lab VM is behind a VPN, so the public site cannot reach it, and a public endpoint on it would expose the lab. (c) Agent E2 as a library inside each app: two copies to keep in step, in Python and in TypeScript.
  - Serves: SCOPE-1, SCOPE-8, PRINCIPLE-5; R-ASK-001, R-E2-015.
- **DESIGN-2 Domain knowledge has one master, in Agent E2.** Agent E2 holds every KPI name, part, limit, scoring rule, threshold, flow and explanation, in its knowledge files and catalog. The VCF vCommunity Adapter implements the KPIs; PCM and isvara.io consume them; isvara.io holds no knowledge of its own. A change to domain knowledge starts in agent-e2, and the adapter follows in the same session.
  - Why: with one master, every other copy is generated from it or checked against it (contract C1).
  - Rejected: (a) the adapter as master of the KPIs, since it computes them: its Python tables hold no explanation, and Agent E2 could not explain a number it does not own. (b) A copy per app: the copies drift (RISK-6).
  - Serves: PRINCIPLE-5, Q-WS-15, Q-WS-18; R-ADP-006, R-CONTENT-004, R-E2-025, R-EXAM-008, R-EXAM-009, R-EXPORT-002, R-KPI-001, R-KPI-002, R-PRACTICE-003, R-REPO-001, R-TOOL-004, R-TOOL-005.
- **DESIGN-3 isvara.io's pages built from Agent E2's knowledge.** isvara.io's articles are AI rewrites of Agent E2's knowledge files, built from an export whose shape is one schema in this workspace (contract C4). Each page passes checks before it is published. The Word books stay as downloads only.
  - Why: isvara.io then holds no copy of the knowledge that could drift (DESIGN-2).
  - Rejected: (a) keep converting the Word books into pages: a second master. (b) Show the knowledge files as they are: they are written for a model, dense and tagged, and the author asked for prose (Q-WS-42). (c) Read agent-e2's repository at run time: a page would reach readers without its checks.
  - Serves: SCOPE-8, ASSUMPTION-7; R-CONTENT-002, R-CONTENT-016, R-E2-027, R-EXPORT-002.
- **DESIGN-4 The workspace specifies where the repositories meet.** This workspace holds the brief, this design, the test plan, the contracts with their checks, and its own tools. Every other requirement, design note and test lives in the repository that implements it, and the workspace's tools read them from clones. A domain fact lives in agent-e2. A workspace requirement on a contract says that two sides are equal and names the check that compares them. "Comes from Agent E2" means that a value is stated in Agent E2 and that the implementing repository's copy equals it; nothing reads the agent-e2 repository at run time.
  - Why: a requirement next to its code changes in the same pull request as the code.
  - Rejected: (a) every requirement in the workspace: each change needs two pull requests in two repositories, and the second is forgotten. (b) Each repository on its own: nobody owns the seams. (c) The adapter reads Agent E2's catalog at run time: it runs inside VCF Operations with no access to GitHub, and a customer may install the pak without Agent E2 (SCOPE-3).
  - Serves: PRINCIPLE-5, PRINCIPLE-6; R-ADP-010, R-CONTENT-001, R-EXPORT-001, R-KPI-001, R-KPI-005, R-KPI-006.

### Maintainability

- **DESIGN-5 Every contract checked by code.** Each contract between two repositories has a check in [`checks/`](../../checks) that compares both sides, and a test that plants a break of each kind it compares. The checks run on every pull request of every repository, daily and on demand. Known gaps sit in a baseline that only shrinks. A contract changes in three steps: add the new shape, move each consumer, remove the old shape.
  - Why: without a check, the two sides of a contract drift apart and nobody notices until something breaks.
  - Rejected: (a) review by reading both sides: each session starts without memory of the last, so drift passes review. (b) A shared library imported by both sides: it couples the releases of a management pack, a Python service and two web apps, and a pak inside VCF Operations cannot import from GitHub. (c) End-to-end tests only: they need the lab (CONSTRAINT-6).
  - Serves: GOAL-4, RISK-6; R-E2-009, R-E2-019, R-EXPORT-001, R-WS-001, R-WS-002, R-WS-008.
- **DESIGN-6 Names a reader can guess.** In every repository, an ID, term, heading, folder or file name can be guessed from itself. Each concept has one word, or two when one would be ambiguous. Names carry no version, milestone or status word, since git keeps the history. A name that stops being true is renamed in every file. isvara's five folder renames happen in M4 with redirects, when the rebuild moves those pages anyway.
  - Why: every session, person or AI, reads the files without memory of earlier ones, so a name that needs explaining costs every reader. The author, 2026-11-27: "The best documentation is No Documentation."
  - Rejected: (a) a naming guide with exceptions: each exception needs explaining again. (b) isvara's renames in M2: the rebuild of M4 would move the same folders a second time.
  - Serves: CONSTRAINT-2, CONSTRAINT-3; R-ADP-025, R-REPO-005 to R-REPO-008, R-WS-007.
- **DESIGN-7 One set of writing rules, checked by code.** Documents for people follow [writing/README.md](../../writing/README.md) and its flagged phrases; documents for machines hold one rule per bullet with exact names. [tools/style.py](../../tools/style.py) checks every repository on its pull requests, against a baseline per repository that only shrinks; agent-e2's lint reads the same list.
  - Why: the author fixed AI-speak in Agent E2 several times, and the author could not tell what a bare short name such as "C3" meant (Q-WS-46). One copy, checked by code, keeps every repository the same.
  - Rejected: (a) a copy of the rules in each repository: the copies drift. (b) Review only: the same phrases came back each time.
  - Serves: SCOPE-8, Q-WS-42, Q-WS-46; R-CONTENT-003, R-CONTENT-005, R-WS-004 to R-WS-006.
- **DESIGN-8 Traceability from the author's input to the code.** The chain runs: the author's answer, a brief item, a requirement with its Why, Source and acceptance criteria, a design choice, a test scenario, an automated test, the code. [tools/spec_check.py](../../tools/spec_check.py) checks each link it can read: every requirement has a Why line and a Source that names an existing answer, brief item or design choice; every requirement has a test scenario; every scenario belongs to a requirement; every brief item and design choice has its ID once, a reason, and only IDs that exist; every contract names its check. [tools/milestone_review.py](../../tools/milestone_review.py) checks that each requirement belongs to one milestone. The link from a scenario to its automated test is written in the scenario and not yet checked ([test plan](../test-plan.md), section Known gaps).
  - Why: each outcome lives once, where it applies, and a check finds a broken link before a reader does. It replaces the decision log, which held each outcome a second time and recorded the author's answers as decisions.
  - Rejected: (a) a decision log beside the specification: double documentation, two places that drift, and a reader who must read both. (b) A requirements tool outside git: the specification would leave the pull request that changes the code.
  - Serves: PRINCIPLE-6, GOAL-3; R-WS-003.

### Security and privacy

- **DESIGN-9 Lab credentials outside the repositories.** On the author's laptop, two DPAPI files in `$HOME\.secrets\`, written by `Export-Clixml`: `vcf-ops-readonly.xml` for reading and validating, and `vcf-ops-admin.xml` for installing and restarting the pack. On the PCM lab VM, `/etc/pcm/pcm.env`, readable by root and group `pcm` only. PCM signs in with the read-only account and checks the lab's certificate.
  - Why: the adapter's scripts used to read an admin login from a file inside the repository folder, one wrong ignore rule away from a commit. DPAPI ties a file to one user on one machine, and a read-only account limits what a bug can do.
  - Rejected: (a) a file in the repository folder, ignored by git: one wrong ignore rule publishes it. (b) A different store per tool: two ways to rotate one password. (c) A secrets service: none runs in the lab, and it adds a dependency to a demo.
  - Serves: CONSTRAINT-6; R-ADP-021, R-ADP-022, R-LAB-004, R-LIVE-007, R-LIVE-031.
- **DESIGN-10 isvara.io's injection guard before Agent E2.** isvara.io keeps its pre-scan and the fence around the visitor's turn, and adds one small model call that reads the fenced turn before Agent E2 is called and flags an instruction aimed at the assistant. A flagged question gets a fixed reply. The public Agent E2 answers only calls that carry a secret known to isvara.io, so nobody can go around the guard and the limits (Q-WS-98). Two batteries prove it: the citation eval passes when every answer to 20 reader questions lists at least one source that opens an article; the injection battery passes with 0 violations, while a one-off formatting request is still honoured.
  - Why: when Agent E2 answers, isvara.io no longer writes the prompt, so Rule 4 of AskIO's prompt, the layer that stops an attack today, has nowhere to live. The author placed the guard in isvara.io (Q-WS-47) and asked for the answers to be explained to readers (Q-WS-136).
  - Rejected: (a) a rule in Agent E2 that the question is data: it puts the guard in Agent E2, against Q-WS-47, and PCM's calls would pay for it. (b) The pre-scan and the fence only: more attacks get through.
  - Serves: SCOPE-8, RISK-5; R-ASK-006, R-ASK-007, R-ASK-012, R-E2-024.
- **DESIGN-11 Contributions through a private, reviewed queue.** A contribution is a correction, an addition or something to review, with a note, one link and up to three files (PNG, JPEG, CSV). It goes to a private queue and is never published automatically; the author decides each week from an AI-sorted list, and accepted items become source notes in agent-e2. Contributors may stay anonymous; credit is shown only with a public profile link, checked at review. No email address is collected. Contributors agree, in one sentence, that they may share it, that it holds no confidential customer data, and that it may be used, changed and published. Files are deleted once processed, and after at most 30 days; no IP address is kept with a contribution. The limits are settings: 3 contributions a day per address, 3 files, 5 MB per image, 2 MB per CSV file, 2,000 characters, 1 link, and 100 contributions a day in total.
  - Why: nothing is published without review, which removes the incentive for spam; no account and no email address keep the barrier low and the personal data nil. The author asked Claude to set these details as the one who knows public websites.
  - Rejected: (a) accounts or email sign-up: a barrier for the vCommunity, and personal data to protect. (b) Publishing after an automatic check: spam and wrong knowledge reach readers. (c) Automatic masking of host names and addresses in release 1.0: unreliable on screenshots; visitors remove them (ASSUMPTION-5).
  - Serves: SCOPE-11, PRINCIPLE-3, RISK-9; R-ASK-003, R-CONTRIB-001 to R-CONTRIB-006, R-PROTECT-001, R-PROTECT-002, R-PROTECT-004, R-PROTECT-006.
- **DESIGN-12 isvara.io's protection layers.** One protection per threat, all in isvara.io: Vercel's platform protection and firewall rate limits against floods; an invisible bot check and a hidden field before Ask and Contribute; limits per address, 10 questions an hour and 30 a day; files checked by their content, image metadata removed, and a model call that keeps only IT screenshots; a daily ceiling on model calls (DESIGN-20); one switch that closes Ask or Contribute without a redeploy. The threats and their protections: [isvara.io plan](isvara-plan.md), section Protection.
  - Why: isvara.io is public, has no sign-in, and each model call costs money.
  - Rejected: (a) sign-in before Ask: it keeps visitors out (PRINCIPLE-1). (b) A firewall product bought apart: Vercel's firewall stops floods on the current plan, which is checked before building.
  - Serves: RISK-4, RISK-5; R-PROTECT-001 to R-PROTECT-006.
- **DESIGN-13 Data the system keeps, and for how long.** PCM stores no metrics; it keeps each Agent E2 answer with its trace ID and rating for 30 days. Agent E2 keeps each answer's trace for 30 days. isvara.io keeps questions and answers with their trace and rating for 30 days, keeps no copy of the files attached to a question, and keeps a contribution's files at most 30 days, with no IP address. Lab facts may go to the cloud model. In the on-premises deployment, nothing leaves the customer's network.
  - Why: a wrong answer can be fixed only when its trace shows the cause: a missed file, a wrong file, or a file the model ignored (Q-WS-61). Thirty days covers the weekly reviews; anything kept longer is a liability (PRINCIPLE-3).
  - Rejected: (a) keep nothing: a wrong answer cannot be diagnosed. (b) Keep everything: personal and customer data with no use.
  - Serves: PRINCIPLE-3, SCOPE-5; R-ASK-009, R-CONTRIB-004, R-E2-023.

### Performance and scalability

- **DESIGN-14 Long answers as jobs with a visible stage.** A caller starts an answer as a job and reads it every 10 seconds. The job reports its stage, such as "reading files", "writing" or "checking", and a time stamp that moves at least every 10 seconds; the browser counts the time up between reads. A job that stops moving for 60 seconds shows a message, and a job ends after 10 minutes with a reason. Jobs live in the memory of one long-running Agent E2 process. A synchronous call stays for PCM's synthetic demo until it moves to jobs (SCOPE-19).
  - Why: an answer may take minutes (SCOPE-6), longer than a browser, a proxy or a serverless function waits on one request, and the user must see that Agent E2 is not hung (Q-WS-I3, Q-WS-57). Reading every 10 seconds shows progress often enough (ASSUMPTION-2) at a cost of a few small calls a minute. The longest answer measured so far took about a minute, so 10 minutes leaves margin (Q-WS-93).
  - Rejected: (a) streaming the answer: the author does not need it (Q-WS-I3), and Agent E2 checks an answer before returning it, so streamed text would reach the reader unchecked. (b) One long synchronous request: Vercel's functions and many proxies cut it. (c) Server-sent events or WebSockets: a connection held open for minutes, which the same functions and proxies cut; a plain read every 10 seconds passes any proxy.
  - Serves: SCOPE-6, ASSUMPTION-2; R-ASK-002, R-E2-007, R-E2-008, R-E2-009, R-E2-010, R-E2-020.
- **DESIGN-15 PCM reads through with a 60-second cache.** PCM's live demo reads VCF Operations through the Suite API when a page asks, keeps each response for 60 seconds, and stores nothing. A page answers in under 5 seconds; each Suite API read stops after 10 seconds; a failed read shows "No data" for the whole page (Q-WS-69).
  - Why: VCF Operations already keeps the history, so a second store would be a stale copy that needs sizing and backup. Sixty seconds is shorter than the 5-minute collection cycle, so the cache never hides a new value for long, and it keeps repeated clicks off the Suite API.
  - Rejected: (a) a metrics store in PCM: SCOPE-5 says PCM stores no metrics. (b) No cache: every tab and refresh reads the Suite API again, slowly on a page with many objects. (c) A cache longer than one collection cycle: it hides new values.
  - Serves: SCOPE-5; R-LIVE-009, R-LIVE-010, R-LIVE-011.
- **DESIGN-16 Hosting of the public Agent E2, chosen by measurement.** In M5, start-up time and cost per answer are measured on a Vercel Python function and on a small container host, and the cheaper option that keeps jobs (DESIGN-14) is chosen. A container host is preferred, because Agent E2 keeps answer jobs in memory.
  - Why: the cost per visitor is unknown (ASSUMPTION-4), and a serverless function can start cold and lose in-memory jobs between calls (Q-WS-94).
  - Rejected: (a) the lab VM: it is behind a VPN, in the author's own lab. (b) Choosing before measuring: the difference in cost is unknown (Q-WS-4).
  - Serves: ASSUMPTION-4, CONSTRAINT-1; R-ASK-007, R-E2-024.

### Correctness

- **DESIGN-17 Missing data never shown as a value.** The VCF vCommunity Adapter publishes no value built from a partial read. PCM shows "No data" for a stale value from the time of the value: 10 minutes for a value, 30 minutes for a check result (Q-WS-64). A part that a cluster does not have is left out of PCM's page until the adapter makes absent data explicit (SCOPE-18). PCM's key list comes from the adapter's module tables, and the lab read confirms it.
  - Why: a partial read gives values that look normal, which is a correctness bug, and a blank is honest (PRINCIPLE-2). The adapter already leaves a metric blank when its input is older than 10 minutes, one collection cycle plus one of margin.
  - Rejected: (a) state codes in release 1.0: useful, but a demo can show "No data" without them (SCOPE-18). (b) Waiting 15 minutes before a value counts as stale: the author asked for no wait (Q-WS-27).
  - Serves: PRINCIPLE-2, SCOPE-5; R-ADP-018, R-ADP-019, R-LIVE-020, R-LIVE-023.
- **DESIGN-18 One Cluster Risk closure level in release 1.0.** Agent E2's knowledge and catalog keep two Cluster Risk levels for Close for Business as practice: production closes above 60%, non-production above 80%. Release 1.0 applies the production level to every cluster. The catalog's production row says it applies to every cluster in release 1.0, and its non-production row says it is not applied in release 1.0. Agent E2's Close for Business file, the adapter's pages and Agent E2's capacity opening state the limitation. Agent E2 reads no `production` fact. The KPI definitions check compares the adapter's level with the production row.
  - Why: no data source says which clusters are production (CONSTRAINT-5). One level lets Agent E2 explain the verdict PCM shows (Q-WS-16), and the production level closes a cluster earlier, which is the safer error.
  - Rejected: (a) two levels with the environment guessed from the cluster's name: as often wrong as right. (b) The non-production level for every cluster: production clusters would close late.
  - Serves: CONSTRAINT-5; R-ADP-011, R-E2-017, R-KPI-006.
- **DESIGN-19 Answers graded automatically.** The free-text answer set (SCOPE-6) is graded by Opus 5.5 as judge, on every change of model or prompt. Claude drafts the questions from the knowledge base and the author's demo questions; an independent agent tries to break each answer key; the author reviews only the keys it marks uncertain, and grades 20 answers once to check that the grader agrees with the author (Q-WS-92). If the first run is far below the target, the gate is set from that run (Q-WS-90).
  - Why: the author has no time to grade each run (CONSTRAINT-8), and confident wrong answers are the main risk (RISK-1).
  - Rejected: (a) the author grades every run: CONSTRAINT-8. (b) The multiple-choice benchmark only: users read free text, which it never checks (Q-WS-5).
  - Serves: GOAL-4, PRINCIPLE-2, RISK-1, ASSUMPTION-3; R-E2-004, R-E2-005, R-E2-006, R-E2-026.

### Cost

- **DESIGN-20 Spending limits built into the system.** isvara.io stops model calls for the day at a ceiling that keeps the month within CONSTRAINT-1; each address has question limits (DESIGN-12); each answer reports its time and tokens, so a benchmark run's cost is known; the model is a setting, so a cheaper one replaces it without a code change.
  - Why: spending is tracked by hand on vercel.com (CONSTRAINT-1); a limit in code acts before the bill arrives.
  - Rejected: (a) watching the bill only: it acts a month late. (b) A monthly ceiling only: one bad day spends the month.
  - Serves: CONSTRAINT-1, RISK-4; R-ASK-010, R-E2-010, R-EXAM-007, R-PROTECT-005.

### Method

- **DESIGN-21 Work only in the open milestone.** Releases and their milestones are set once, in the workspace's [ROADMAP.md](../../ROADMAP.md), for every repository at once; a child repository names the workspace milestone it serves and no release of its own. The milestones of release 1.0 are M1 to M8, in the order of work, one outcome each. Work happens only in the open milestone, the first whose heading does not end with ": done", and a milestone is marked done only after the author approves it. No file of this repository and no requirement belongs to two milestones. [tools/milestone_gate.py](../../tools/milestone_gate.py) prints the open milestone at every prompt, through the hook in [.claude/settings.json](../../.claude/settings.json), and fails a pull request that changes a file owned only by a later milestone; [tools/milestone_review.py](../../tools/milestone_review.py) fails a requirement in no milestone or in two. All lab work is in M8; before it, a session runs every test that works with fakes and lists each lab check it could not run for M8's lab session.
  - Why: the agent worked ahead of the open milestone three times between 2026-11-25 and 2026-11-27, and a rule with a check behind it holds where a rule in prose did not. The author: "Release should only apply at the Workspace level, not individual component repository. We work on all these repository as a set."
  - Rejected: (a) a narrow rule for each case found: three were added and the next case was new. (b) Milestones per repository: the repositories are released as one set, and their milestones would overlap.
  - Serves: GOAL-5, DEPENDENCY-1, CONSTRAINT-6, RISK-3; R-WS-003.
- **DESIGN-22 One method file in every repository.** Every repository holds the same CLAUDE.md, which states the method of spec-driven development for any project, and its own CLAUDE-PROJECT.md for this project's tools, paths, domain and lab, imported by CLAUDE.md. [tools/claude_md_copies.py](../../tools/claude_md_copies.py) fails when a repository's CLAUDE.md differs from the workspace's. The method's rules live in the repositories, where the author's team can read them, and nowhere private.
  - Why: each session starts in one repository and reads only its files, so the method must be in each; and the author wants a method that applies to future projects unchanged: "The Claude.md should be universal claude setting."
  - Rejected: (a) the method in the workspace only: a session in a child repository would not read it. (b) Project rules in CLAUDE.md: the file would not carry over to another project. (c) Private instructions or memory: the author's team cannot see them.
  - Serves: PRINCIPLE-6, GOAL-3.
- **DESIGN-23 Questions kept where they bind, with IDs that name the repository.** A question about one repository stays in that repository's question file; one that binds several goes to the workspace's [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md). An ID names its repository: `Q-WS-n` in the workspace (`Q-WS-In` for the author's intent), `Q-E2-nnn` in agent-e2, `Q-ADP-n` in PCM-Adapter, `Q-PCM-n` in private-cloud-manager and `Q-ISVARA-n` in isvara. A question asks the author only for input (a goal, scope, requirement, assumption, constraint, reason or fact from the field) and carries Claude's working assumption, which the work follows until the author answers.
  - Why: the workspace's Q-120 and agent-e2's Q120 were two different questions; and the author's answer is input to the specification, while the design is Claude's (Q-WS-13).
  - Rejected: (a) one question file for every repository: a session in one repository reads questions it cannot act on. (b) Numbers without a prefix: the same number named two questions. (c) A recommendation that waits for the author's approval: it stalls the work and asks the author for a design call.
  - Serves: CONSTRAINT-8, PRINCIPLE-6.
