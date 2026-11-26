# Glossary

Every short name and ID used in this workspace, with what it means and where it is defined. A document uses an ID only with its meaning on first use, or as a link to this page (DECISIONS, W-020).

## IDs

| ID | Meaning | Defined in |
|---|---|---|
| <a id="c1"></a>C1 | Contract 1, **KPI definitions**: each KPI's names, parts, limits and scoring | [CONTRACTS.md](../CONTRACTS.md) |
| <a id="c2"></a>C2 | Contract 2, **KPI metric keys**: the keys PCM-Adapter publishes in VCF Operations and PCM reads | [CONTRACTS.md](../CONTRACTS.md) |
| <a id="c3"></a>C3 | Contract 3, **the Agent E2 API**: the HTTP calls PCM and isvara.io make to Agent E2 | [CONTRACTS.md](../CONTRACTS.md) |
| <a id="c4"></a>C4 | Contract 4, **knowledge content for isvara.io**: what Agent E2 gives isvara.io to build its pages from | [CONTRACTS.md](../CONTRACTS.md) |
| <a id="c5"></a>C5 | Contract 5, **the model gateway**: Vercel AI Gateway, through which Agent E2 calls its model | [CONTRACTS.md](../CONTRACTS.md) |
| W-001 to W-0nn | A decision that binds more than one repository | [DECISIONS.md](../DECISIONS.md) |
| D-001 to D-1nn | A decision inside PCM | [PCM decisions.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md) |
| Q-1, Q-I1 and so on | A question in the interview; Q-I questions are about intent | [Round 1](interview-round-1.md), [open questions](../OPEN-QUESTIONS.md) |
| M0 to M7 | A milestone of the roadmap | [ROADMAP.md](../ROADMAP.md) |
| R-AREA-nnn | A requirement, for example R-LIVE-003 | [requirements/](requirements) |
| T-AREA-nnnx | A test scenario of a requirement, for example T-LIVE-003a | [requirements/](requirements) |

## Words

| Word | Meaning |
|---|---|
| Stage 1 | Now: PCM as a lab demo, a cloud model, isvara.io public on Vercel |
| Stage 2 | Later, out of scope: customers run everything on premises, with a local model |
| ACME | The synthetic customer, a global bank, whose data PCM generates for the main demo |
| Live demo | PCM's L2 workspace on the author's lab VCF Operations; its own demo entry |
| L2 | The platform engineer role in PCM, the expert behind the NOC |
| VCF Operations | VMware Cloud Foundation Operations, the monitoring product; lab at https://10.115.1.81 |
| Suite API | VCF Operations' REST API, which PCM and the PCM-Adapter tools read |
| PCM-Adapter | The management pack inside VCF Operations that computes the KPIs; formerly VCF-vCommunity-Adapter |
| Catalog | Agent E2's [knowledge/catalog](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge/catalog) YAML files, master of every KPI definition |
| KPI | A 0 to 100% score built from several sub-metrics (parts), for example Cluster Performance |
| Part, sub-metric | One input of a KPI, with five limits that set its score |
| Metric key | The identifier VCF Operations uses for a metric, set by PCM-Adapter; what the Suite API returns |
| Metric name | The words a person reads for a metric, set by Agent E2's catalog |
| Peak metric | Named "peak": the highest 20-second value of each 5-minute cycle |
| Check | Code in [checks/](../checks) or [tools/](../tools) that proves a contract or a rule, run in CI |
| Baseline | A list of known gaps a check reports without failing; it may only shrink |
