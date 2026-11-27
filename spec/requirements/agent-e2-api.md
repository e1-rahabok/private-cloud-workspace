# Requirements: the Agent E2 API

Contract [C3, the Agent E2 API](../glossary.md#c3): the HTTP calls PCM and isvara.io make to Agent E2. Agent E2 owns the shape, written in the docstring of [harness/answer_service.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py); the workspace keeps the requirements on the contract and its check, [checks/agent_e2_api.py](../../checks/agent_e2_api.py) ([WD-036](../../DECISIONS.md)). What Agent E2 does behind the API is in agent-e2's [answer-service.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/requirements/answer-service.md). Question IDs (Q-) point at the interview: [round 1](../interview-round-1.md), [round 2](../interview-round-2.md). Other IDs are explained in the [glossary](../glossary.md). These requirements belong to milestone M3 in [ROADMAP.md](../../ROADMAP.md).

## Time and progress

### R-E2-009 The synchronous call keeps working until both callers have moved

Source: WD-010 (every contract has a check; changes go expand, migrate, contract); WD-013.

- Given PCM's client, which calls `/v1/answer` and waits up to 180 seconds ([agent_e2.py](https://github.com/e1-rahabok/private-cloud-manager/blob/main/build/pcm_proto/agent_e2.py#L105))
- When the job calls of R-E2-007 are added
- Then a call without `"async"` still returns the answer in one reply, with every field it has today
- And PCM's live demo and isvara.io each move to the job calls in their own pull request
- And PCM's synthetic demo keeps the synchronous call in release 1.0, unchanged (R-LIVE-032); the synchronous form is removed after release 1.0, once that demo has moved too

Test scenarios:
- T-E2-009a (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py)): the check as it runs today, through PCM's client, passes after the job calls are added.

## Facts PCM sends

### R-E2-017 The specification lists the facts each answer feature needs

Source: answer to Q-WS-36 ("agree": C3's specification lists the facts each feature needs; C3's check adds a live-shaped case; Agent E2 says when a needed fact is missing).

- Given the docstring of [answer_service.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py), the specification of the Agent E2 API
- When it is read
- Then it has one table: each feature, the facts it needs, and what Agent E2 does without them
- And the table starts from these features, with the fact names PCM sends today ([frame.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/workspaces/l2/frame.md)):

| Feature | Facts it needs | Without them |
|---|---|---|
| The opening on how a score moved (`lead`) | `kpis`: `label`, `better`, `points` | No opening |
| When a score changed level, and which parts moved | `kpis` points over at least 2 hours; `parts_hourly` for the parts | No step line; no parts named |
| The part that pulled a score down at its worst point | `asked_about_kpi.parts_at_worst` | No part named |
| The capacity opening (close for business) | `pillar: Capacity`; `check` (the Periodic Cluster Check values) or the Consumption, Performance and Risk series; `production` | No capacity opening |
| The band of each figure on the screen | each metric's name, as in the catalog, and its value | No band line |
| Where to look next | `screen.drill_down` | No pointer |
| Suggested questions | `object.kind`, `pillar`, `kpis` | No suggestion |

Test scenarios:
- T-E2-017a (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py), to extend): parse the table from the docstring; every fact name in it appears in PCM's frame.md; every feature has a row.

## The contract check

### R-E2-019 The contract check covers both callers and every new field

Source: WD-010; answer to Q-WS-I1 ("I expect you to check all the contracts").

- Given the Agent E2 service in mock mode (no model, no network)
- When [checks/agent_e2_api.py](../../checks/agent_e2_api.py) runs
- Then it calls the service as PCM does, through PCM's client, and as isvara.io does: until isvara.io has its own client, with a call the check builds from the specification
- And it checks the fields of R-E2-007, R-E2-010, R-E2-012, R-E2-016, R-E2-018, R-E2-022 (`page`, the `reader` role) and R-E2-023 (`trace_id`) by name and type, and the 401 of R-E2-024 when a secret is set

Test scenarios:
- T-E2-019a (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py), to extend): the check passes on agent-e2's main branch.
- T-E2-019b (anywhere, manual once per new field): remove the field in a copy of the service; the check fails and names it.
