# Requirements: KPI definitions

One definition of each KPI, owned by Agent E2's catalog and implemented by PCM-Adapter, shown by PCM and isvara.io. This is contract [C1, KPI definitions](../glossary.md#c1). Question IDs (Q-) point at the interview: [round 1](../interview-round-1.md), [round 2](../interview-round-2.md), [round 3](../interview-round-3.md). R-KPI-001 to R-KPI-007 belong to milestone M2; R-KPI-008 to M8.

Files involved:

- The master: [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml), [thresholds-risk.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-risk.yaml), [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml).
- The implementation: [Management Pack/app/metrics](https://github.com/e1-rahabok/PCM-Adapter/tree/main/Management%20Pack/app/metrics) in PCM-Adapter.
- The check: [checks/kpi_definitions.py](../../checks/kpi_definitions.py).

### R-KPI-001 Every KPI part has one complete row in the catalog

Source: WD-001; answers to Q-1, Q-15 and Q-19 (round 1); Q-81 and Q-89 (round 2: the interval decides the statistic; a key column in every row).

Given any KPI that PCM-Adapter publishes (Cluster Performance, ESXi Performance, VM Performance, Guest OS Performance, Cluster Risk, Cluster Consumption)
When its catalog rows are read
Then each part has exactly one row with: its name, its metric key, its unit, its statistic (20-second peak or 5-minute average), its group, its direction, five limits and whether it is excluded while green
And the statistic agrees with the name: a name with "peak" is a 20-second peak, any other a 5-minute average
And the Guest OS run queue row is named "Peak run queue length per vCPU" (Q-88, round 3), since its limits apply per vCPU

Test scenarios:
- T-KPI-001a (anywhere, automated by checks/kpi_definitions.py, to extend): read every KPI row; fail on a missing field, a duplicate name or key, or a statistic that disagrees with the name.

### R-KPI-002 PCM-Adapter computes each part with the catalog's limits

Source: WD-001; answers to Q-15 and Q-16.

Given a part in the catalog
When PCM-Adapter's KPI module for that KPI is read
Then the adapter has the part, with the same five limits and the same "excluded while green" setting
And the adapter has no part that the catalog lacks

Test scenarios:
- T-KPI-002a (anywhere, automated by checks/kpi_definitions.py): compare every part; any difference fails. Runs in CI today for all 49 parts of the 6 KPIs.
- T-KPI-002b (anywhere, automated by checks/kpi_definitions.py): plant a changed limit in a copy of the catalog; the check must fail and name the part.

### R-KPI-003 Keys come from the adapter, names from the catalog

The contract side. PCM-Adapter's side is [R-ADP-006](pcm-adapter.md); this requirement holds the catalog and the check, that one the code.

Source: answer to Q-1 ("For key, adapter is correct. For name, Agent E2 is correct"); Q-89 (round 2).

Given a part
When it is published in VCF Operations and shown in PCM
Then its metric key is the key in the catalog row, which is the key PCM-Adapter publishes
And the name a person reads, in VCF Operations and in PCM, is the catalog's name

Test scenarios:
- T-KPI-003a (anywhere, automated by checks/kpi_definitions.py, to extend): match parts by key; fail when an adapter label differs from the catalog name. The baseline of 11 VM and Guest OS name gaps must be empty.
- T-KPI-003b (lab, automated by PCM-Adapter's tools/screenshot): after installing the pack, a screenshot of one VM's metric list shows the catalog names.

### R-KPI-004 The scoring rules are defined once, in the catalog, with worked examples

The contract side. PCM-Adapter's side is [R-ADP-009](pcm-adapter.md); this requirement holds the catalog and the check, that one the code.

Source: answers to Q-14 and Q-15 ("All their logic should come from Agent E2"); Q-87 (round 2: the formula is part of C1).

Given the scoring rules (how a part's value becomes a score, how parts are weighted, how values are rounded, what happens to a part with no data, how "excluded while green" works)
When the catalog is read
Then each rule is stated once, with at least one worked example per rule: the input values and the expected score
And PCM-Adapter's scoring code returns each example's expected score exactly

Test scenarios:
- T-KPI-004a (anywhere, automated by checks/kpi_definitions.py, to extend): run every worked example through the adapter's `kpi_score.py`; any difference fails.
- T-KPI-004b (anywhere): plant a changed weight in a copy of the adapter's code; the check must fail.

### R-KPI-005 Every KPI score has its bands in the catalog

The contract side. PCM-Adapter's side is [R-ADP-010](pcm-adapter.md); this requirement holds the catalog and the check, that one the code.

Source: answer to Q-15.

Given any KPI score, including Cluster Performance
When its colour is decided, in VCF Operations, in PCM or in isvara.io
Then the bands come from a score row in the catalog
And PCM-Adapter's band table equals it

Test scenarios:
- T-KPI-005a (anywhere, automated by checks/kpi_definitions.py, to extend): every KPI has a score row; the adapter's bands equal it.

### R-KPI-006 The Periodic Cluster Check uses the catalog's closure levels

The contract side. PCM-Adapter's side is [R-ADP-011](pcm-adapter.md); this requirement holds the catalog and the check, that one the code.

Source: answers to Q-15 and Q-16.

Given a cluster
When the Periodic Cluster Check decides whether it is closed for new VMs
Then the closure levels for Consumption, Performance and Risk come from the catalog
And one Risk level applies to every cluster, production or not

Test scenarios:
- T-KPI-006a (anywhere, automated by checks/kpi_definitions.py, to extend): the adapter's closure levels equal the catalog's; the catalog has one Risk level.
- T-KPI-006b (anywhere, automated by PCM-Adapter's unit tests): a cluster just above and just below each level opens or closes as the catalog says.

### R-KPI-007 Usable capacity is Total − HA − Buffer

The contract side. PCM-Adapter's side is [R-ADP-012](pcm-adapter.md); this requirement holds the catalog and the check, that one the code.

Source: answer to Q-17.

Given a cluster's capacity
When usable capacity is computed for Cluster Consumption
Then it is total capacity minus the HA reservation minus the buffer, in the catalog and in the adapter
And PCM-Adapter issue #14 is closed

Test scenarios:
- T-KPI-007a (anywhere, automated by PCM-Adapter's unit tests): a cluster with known total, HA and buffer gives the expected usable capacity and Consumption score.

### R-KPI-008 isvara.io holds no KPI numbers of its own

Source: answer to Q-18 ("isvara.io should never have its own knowledge").

Given any number isvara.io uses about performance or capacity (a limit, a band, an overcommit ratio, a class of service)
When isvara.io is built
Then the number is generated from the catalog
And no such number is written by hand in isvara.io's code

Test scenarios:
- T-KPI-008a (anywhere, automated by a check to write, checks/isvara_numbers.py): isvara.io's generated module equals the catalog; a hand-written threshold constant in its code fails the check.

## Questions for round two

- None.
