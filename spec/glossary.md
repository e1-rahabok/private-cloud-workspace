# Glossary

Every short name and ID used in this workspace, with what it means and where it is defined. A document uses an ID only with its meaning on first use, or as a link to this page (R-WS-005).

## IDs

| ID | Meaning | Defined in |
|---|---|---|
| <a id="c1"></a>C1 | Contract 1, **KPI definitions**: each KPI's names, parts and limits | [contracts](design/system.md#contracts) |
| <a id="c2"></a>C2 | Contract 2, **KPI metric keys**: published by the VCF vCommunity Adapter, read by PCM | [contracts](design/system.md#contracts) |
| <a id="c3"></a>C3 | Contract 3, **the Agent E2 API**: the HTTP calls PCM and isvara.io make to Agent E2 | [contracts](design/system.md#contracts) |
| <a id="c4"></a>C4 | Contract 4, **knowledge content for isvara.io**: what Agent E2 gives isvara.io to build its pages from | [contracts](design/system.md#contracts) |
| <a id="c5"></a>C5 | Contract 5, **the model gateway**: Vercel AI Gateway, through which Agent E2 calls its model | [contracts](design/system.md#contracts) |
| GOAL-n | A goal of the product or of release 1.0, with its reason and source | [brief.md](brief.md) |
| SCOPE-n | What release 1.0 holds, or what waits until after it | [brief.md](brief.md) |
| PRINCIPLE-n | A rule that decides a conflict between two good things | [brief.md](brief.md) |
| CONSTRAINT-n | A limit the design must respect: budget, identity, lab, time | [brief.md](brief.md) |
| ASSUMPTION-n | Something taken as true, with its status and how it is checked | [brief.md](brief.md) |
| RISK-n | What could go wrong, its effect, what reduces it and who acts | [brief.md](brief.md) |
| DEPENDENCY-n | What the work needs from people or systems outside Claude's reach | [brief.md](brief.md) |
| DESIGN-n | A design choice, with its reason, the options rejected and what it serves | [design/system.md](design/system.md) |
| WD-001 to WD-046 | A decision of the retired decision log; git history keeps it | Outcomes: [brief](brief.md), [system design](design/system.md) |
| D-001 to D-1nn | A decision inside PCM | [PCM decisions.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md) |
| Q-WS-1, Q-WS-I1 and so on | A question to the author about the workspace; Q-WS-I questions are about intent | Rounds [1](author-input/interview-round-1.md), [2](author-input/interview-round-2.md), [3](author-input/interview-round-3.md), [4](author-input/interview-round-4.md), [5](author-input/interview-round-5.md); [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) |
| Q-E2-001 and so on | A question to the author about agent-e2 | [agent-e2 author-questions.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/author-questions.md) |
| Q-PCM-1 and so on | A question to the author about private-cloud-manager only (DESIGN-23) | [private-cloud-manager OPEN-QUESTIONS.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/OPEN-QUESTIONS.md); answers in its [decisions.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md) |
| Q-ADP-1 and so on | A question to the author about PCM-Adapter only (DESIGN-23) | [PCM-Adapter OPEN-QUESTIONS.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/OPEN-QUESTIONS.md) |
| Q-ISVARA-1 and so on | A question to the author about isvara only (DESIGN-23) | [isvara OPEN-QUESTIONS.md](https://github.com/e1-rahabok/isvara/blob/main/OPEN-QUESTIONS.md) |
| M1 to M8 | A roadmap milestone of release 1.0, numbered from M1 in the order of work (DESIGN-21) | [ROADMAP.md](../ROADMAP.md) |
| A1 to A6 | A milestone of agent-e2's plan toward its part of release 1.0 (Q-WS-58) | [agent-e2 plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) |
| R-AREA-nnn | A requirement, for example R-LIVE-003 | [requirements/](requirements) |
| T-AREA-nnnx | A test scenario of a requirement, for example T-LIVE-003a | [requirements/](requirements) |

## Words

| Word | Meaning |
|---|---|
| PCM | Private Cloud Manager, the web app (CONSTRAINT-3) |
| SP5 | The author's operations framework: availability, performance, security, capacity, value ([Agent E2's files](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge/sp5-framework)) |
| E1, E2 | E1: the author, Iwan Rahabok. E2: version 2.0 of him, available 24/7 |
| Release 1.0 | The goal: PCM as a lab demo, a cloud model, isvara.io public on Vercel |
| Release | A scope of work for all repositories at once, set only in the roadmap (DESIGN-21) |
| Milestone | A step toward release 1.0 in the roadmap |
| On-premises deployment | After release 1.0, out of scope: customers run everything on premises, with a local model |
| Stage 1, stage 2 | In the interview records: release 1.0, and the on-premises deployment |
| The Book | Private Cloud Management, 5th edition: four Parts and an Executive Summary. 6th edition planned for 2027 |
| ACME | The synthetic customer, a global bank, whose data PCM generates for the main demo |
| Live demo | PCM's L2 workspace on the author's lab VCF Operations; its own demo entry |
| L2 | The platform engineer role in PCM, the expert behind the NOC |
| VCF Operations | VMware Cloud Foundation Operations, the monitoring product; the lab has one, reached over the VPN |
| Suite API | VCF Operations' REST API, which PCM and the VCF vCommunity Adapter tools read |
| PCM-Adapter | The repository of the VCF vCommunity Adapter |
| VCF vCommunity Adapter | The management pack in VCF Operations that computes the KPIs of PCM's scenario 7 ([system design](design/system.md)) |
| Review page | One page per milestone, [spec/review](review), in plain words, for the author's approval (R-WS-015) |
| Slice | A thin piece of a milestone, end to end, for one narrow case |
| Learning path | One of isvara.io's three ways into the knowledge: Architecture, IT management, Product ([knowledge model](design/knowledge-model.md)) |
| Lens | One of four ways to know a topic ([knowledge model](design/knowledge-model.md)) |
| Demo scenario | One entry of PCM's demo control; 7 is live, 1 to 6 synthetic |
| PCM scenario story | A condition planted in PCM's synthetic data, with the result each workspace must show (PCM D-132) |
| Catalog | Agent E2's [knowledge/catalog](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge/catalog) YAML files, master of every KPI definition |
| KPI | A 0 to 100% score built from several sub-metrics (parts), for example Cluster Performance |
| Part, sub-metric | One input of a KPI, with five limits that set its score |
| Metric key | A metric's identifier in VCF Operations, as the Suite API returns it |
| Metric name | The words a person reads for a metric, set by Agent E2's catalog |
| Peak metric | Named "peak": the highest 20-second value of each 5-minute cycle |
| Check | Code in [contract-checks/](../contract-checks) or [tools/](../tools) that proves a contract or a rule, run in CI |
| Baseline | A list of known gaps a check reports without failing; it may only shrink |
