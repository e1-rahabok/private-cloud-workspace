# Requirements: KPI definitions

Contract [C1, KPI definitions](../glossary.md#c1): the KPI tables in the VCF vCommunity Adapter's code equal the rows of Agent E2's catalog, and a workspace check compares them. The catalog holds data: for each part of a KPI, its name, key, unit, interval, five limits and whether it is excluded while green, plus the score bands and the close-for-business levels. How a score is computed is domain knowledge, explained in Agent E2's [performance-kpi-design.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/performance-kpi-design.md) and implemented and tested in the adapter's [kpi_score.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/kpi_score.py); neither is specified here (DESIGN-4). Question IDs (Q-) point at the interview: [round 1](../author-input/interview-round-1.md), [round 2](../author-input/interview-round-2.md), [round 3](../author-input/interview-round-3.md). R-KPI-001 to R-KPI-006 belong to milestone M2. Other IDs are explained in the [glossary](../glossary.md).

Files involved:

- The master: [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml), [thresholds-risk.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-risk.yaml), [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml).
- The implementation: [Management Pack/app/metrics](https://github.com/e1-rahabok/PCM-Adapter/tree/main/Management%20Pack/app/metrics) in PCM-Adapter.
- The check: [contract-checks/kpi_definitions.py](../../contract-checks/kpi_definitions.py).

### R-KPI-001 Every part the adapter publishes has a catalog row with a key

Why: a part without a catalog row has no master, so its limits and name drift.

Source: DESIGN-2; answers to Q-WS-1 and Q-WS-19 (round 1); Q-WS-89 (round 2: a key column in every row); DESIGN-4.

- Given any KPI that the VCF vCommunity Adapter publishes (Cluster Performance, ESXi Performance, VM Performance, Guest OS Performance, Cluster Risk, Cluster Consumption)
- When the check reads Agent E2's catalog
- Then each part of the KPI has exactly one catalog row, with the fields the comparison needs: name, key, five limits for at least one interval, and the unit in the name when the metric has one; and the excluded-while-green flag, which a row leaves out when it is false

Test scenarios:
- T-KPI-001a (anywhere, automated by contract-checks/kpi_definitions.py): for every part the adapter publishes, find its catalog row by key; fail on a missing row, a missing field or two rows with one key.

### R-KPI-002 Each part's limits in the adapter equal the catalog's

Why: the adapter scores with its own copy of the limits, so a change in the catalog must reach it.

Source: DESIGN-2; answers to Q-WS-15 and Q-WS-16.

- Given a part in the catalog
- When VCF vCommunity Adapter's KPI module for that KPI is read
- Then the adapter has the part, with the same five limits and the same "excluded while green" setting
- And the adapter has no part that the catalog lacks

Test scenarios:
- T-KPI-002a (anywhere, automated by contract-checks/kpi_definitions.py): compare every part; any difference fails. Runs in CI today for all 49 parts of the 6 KPIs.
- T-KPI-002b (anywhere, automated by contract-checks/kpi_definitions.py): plant a changed limit in a copy of the catalog; the check must fail and name the part.

### R-KPI-003 Each part's key and name agree between catalog and adapter

The contract side. VCF vCommunity Adapter's side is [R-ADP-006](https://github.com/e1-rahabok/PCM-Adapter/blob/main/spec/requirements/adapter.md#r-adp-006-a-metrics-label-equals-the-agent-e2-catalog-name); this requirement holds the catalog and the check, that one the code.

Why: a key or name that differs between the two shows one part under two names.

Source: answer to Q-WS-1 ("For key, adapter is correct. For name, Agent E2 is correct"); Q-WS-89 (round 2).

- Given a part
- When it is published in VCF Operations and shown in PCM
- Then the key in its catalog row equals the key the VCF vCommunity Adapter publishes
- And the label in the adapter's code equals the catalog row's name without its unit

Test scenarios:
- T-KPI-003a (anywhere, automated by contract-checks/kpi_definitions.py): match parts by key; fail when an adapter label differs from the catalog name. The baseline of 11 VM and Guest OS name gaps must be empty.
- Its lab check, a screenshot of one lab cluster's and one lab VM's metric list after installing the pack, is T-ADP-026a in M8 ([R-ADP-026](https://github.com/e1-rahabok/PCM-Adapter/blob/main/spec/requirements/adapter.md#r-adp-026-the-installed-pack-matches-the-catalog-on-the-lab)).

### R-KPI-004 Dropped: the scoring rules are defined once, in the catalog

Source: DESIGN-4.

Dropped by DESIGN-4. The catalog holds data and cannot hold rules. The scoring model is explained in Agent E2's knowledge and implemented and tested in the adapter's code.

### R-KPI-005 Each KPI's score bands equal the catalog's score row

The contract side. The VCF vCommunity Adapter's side is [R-ADP-010](https://github.com/e1-rahabok/PCM-Adapter/blob/main/spec/requirements/adapter.md#r-adp-010-the-score-bands-equal-the-catalogs-score-rows).

Why: PCM shows the adapter's score bands, and the author's knowledge sets them in the catalog.

Source: answer to Q-WS-15; DESIGN-4.

- Given a KPI with a score row in Agent E2's catalog
- When the check compares it with the band table in the adapter's code
- Then the adapter's band limits equal the catalog's score limits
- And a KPI the adapter colours with no score row in the catalog fails the check

Test scenarios:
- T-KPI-005a (anywhere, automated by contract-checks/kpi_definitions.py): compare every score row with the adapter's band table; any difference fails.

### R-KPI-006 The close-for-business levels equal the catalog's

The contract side. The VCF vCommunity Adapter's side is [R-ADP-011](https://github.com/e1-rahabok/PCM-Adapter/blob/main/spec/requirements/adapter.md#r-adp-011-the-closure-levels-equal-the-catalogs).

Why: a different level in the adapter would close a cluster for business at another point than the knowledge says.

Source: answers to Q-WS-15 and Q-WS-16; DESIGN-4; DESIGN-18 (one Risk level for every cluster in release 1.0).

- Given the close-for-business levels in Agent E2's catalog
- When the check compares them with the levels in the adapter's Periodic Cluster Check code
- Then each level for Consumption and Performance is equal
- And the adapter's one Risk level equals the catalog's production row, `closure-cluster-risk-prod`, which the catalog says release 1.0 applies to every cluster; the non-production row is not compared

Test scenarios:
- T-KPI-006a (anywhere, automated by contract-checks/kpi_definitions.py): compare every level, Risk against the production row; any difference fails. A planted break of each level is in contract-checks/test_kpi_definitions.py.

### R-KPI-007 Dropped: usable capacity is Total − HA − Buffer

Source: DESIGN-4.

Dropped by DESIGN-4. The formula is domain knowledge in Agent E2's [cluster-consumption.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md), implemented and tested in the adapter (`test_consumption_is_against_usable_capacity`).

### R-KPI-008 Dropped: isvara.io holds no KPI numbers of its own

Source: DESIGN-4.

Dropped by DESIGN-4: it describes how isvara.io is built, so it moved to [R-CONTENT-001](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/content.md).

## Questions for round two

- None.
