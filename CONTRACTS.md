# Contracts

Every interface between two repositories. Each has one owner, its consumers, where its shape is written, and the check that proves both sides still agree. Every contract has a check, or a milestone that adds one, because an unchecked contract drifts without anyone noticing. The IDs C1 to C5 are also in the [glossary](spec/glossary.md); requirements per contract are in [spec/requirements](spec/requirements).


| ID | Contract                     | Owner, then consumers              | Check                                                             |
| -- | ---------------------------- | ---------------------------------- | ----------------------------------------------------------------- |
| C1 | KPI definitions              | agent-e2; VCF vCommunity Adapter, PCM, isvara | [`checks/kpi_definitions.py`](checks/kpi_definitions.py), running |
| C2 | KPI metric keys              | VCF vCommunity Adapter; PCM (live demo)       | Planned in ROADMAP M8                                             |
| C3 | Agent E2 API                 | agent-e2; PCM, isvara (planned)    | [`checks/agent_e2_api.py`](checks/agent_e2_api.py), running       |
| C4 | Knowledge content for isvara | agent-e2; isvara                   | `checks/knowledge_export.py`, planned in ROADMAP M4          |
| C5 | Model gateway                | Vercel AI Gateway; agent-e2        | None: a third-party API                                           |

## C1 KPI definitions

- **Owner:** agent-e2, [`knowledge/catalog/thresholds-performance.yaml`](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) (section `kpi`), `thresholds-risk.yaml` and `thresholds-capacity.yaml` (section `model`). One row per sub-metric: name with unit, group, direction, five limits per interval, `excluded_when_green`.
- **Implementer:** VCF vCommunity Adapter, `Management Pack/app/metrics/`: one module per KPI, a `METRICS` table of `Metric` rows (name, unit, five limits, `skip_when_green`) and a `LABELS` table that gives a row its catalog name.
- **Consumer:** PCM shows the parts under the catalog names (PCM D-113, D-115) in [`spec/catalog/l2.yaml`](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/catalog/l2.yaml). Not checked yet: PCM names parts in prose (ROADMAP M2).
- **The check** matches each sub-metric by name (the adapter's label against the catalog name without its unit) and compares the five limits and excluded-when-green, for Cluster Performance, ESXi Performance, VM Performance, Guest OS Performance, Cluster Risk and Cluster Consumption.
- **To change a KPI:** change Agent E2's knowledge file and catalog first, then the VCF vCommunity Adapter, in the same session, with the check run before both merges.
- **Status:** limits and excluded-when-green agree for every sub-metric; the known name gaps are to close by [R-KPI-003](spec/requirements/kpi-definitions.md). [`checks/run_all.py`](checks/run_all.py) prints the counts.

## C2 KPI metric keys

- **Owner:** the VCF vCommunity Adapter (repository PCM-Adapter). Keys are `vCommunity|<KPI>|<sub-metric or score>`, for example `vCommunity|Cluster Performance|Cluster Performance Score`, on the vCenter objects in VCF Operations.
- **Consumer:** PCM's demo scenario 7 (live) reads them through the VCF Operations Suite API (PCM D-064, D-096). PCM never connects to the adapter itself; without the adapter installed, scenario 7 has no KPI data.
- **Check, ROADMAP M8:** PCM lists every key it reads in one structured file; the check confirms each key is one the adapter publishes, and, against the lab, that it has data.
- **Status:** no PCM connector yet.

## C3 Agent E2 API

- **Owner:** agent-e2, [`harness/answer_service.py`](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py) (its docstring is the specification). Endpoints: `POST /v1/answer`, `POST /v1/topic`, `POST /v1/suggest` (page and card), `GET /v1/health`.
- **Consumer:** PCM, [`build/pcm_proto/agent_e2.py`](https://github.com/e1-rahabok/private-cloud-manager/blob/main/build/pcm_proto/agent_e2.py), generated from [`spec/catalog/settings.yaml`](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/catalog/settings.yaml) and [`spec/workspaces/l2/frame.md`](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/workspaces/l2/frame.md).
- **The check** starts the real service in mock mode (no model, no network) and calls it with PCM's own client code. It checks every field PCM reads, by name and type, on the raw responses: PCM's client turns errors into `source: unavailable`, which would hide a broken contract.
- **Status:** running; [`checks/run_all.py`](checks/run_all.py) prints the endpoints and the differences.

## C4 Knowledge content for isvara

- Agent E2's knowledge base becomes the source of isvara.io's reading pages, replacing the Word books (DECISIONS, WD-005). Its structure is built for a model to read, so the shape of the export is design work (ROADMAP M1), built in ROADMAP M4.
- **Shape:** one schema in this workspace, `checks/knowledge_export_schema.json`, that agent-e2's export and isvara.io's build both check against ([knowledge-export.md](spec/requirements/knowledge-export.md)).
- **Status:** not built; planned in ROADMAP M4.

## C5 Model gateway

- **Owner:** Vercel AI Gateway, an OpenAI-compatible service; Agent E2 calls it with the key `AI_GATEWAY_API_KEY`.
- **Status:** no check; it is a third-party API.

## Changing a contract

1. **Expand:** the owner adds the new shape and keeps the old one working.
2. **Migrate:** each consumer moves to the new shape, one pull request per repository.
3. **Contract:** the owner removes the old shape.

The checks pass after every step. A pull request that breaks a check is not merged.
