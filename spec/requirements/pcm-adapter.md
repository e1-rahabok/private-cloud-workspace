# VCF vCommunity Adapter requirements

What [PCM-Adapter](https://github.com/e1-rahabok/PCM-Adapter) must do in release 1.0, written from the author's answers in [interview round 1](../interview-round-1.md) and the decisions in [DECISIONS.md](../../DECISIONS.md). Short names and IDs are explained in the [glossary](../glossary.md).

**Draft for the author's review.** The pack keeps its identity: adapter kind `vCommunity`, display name "VCF vCommunity Adapter" and key prefix `vCommunity|` ([WD-032](../../DECISIONS.md)).

## Scope and conventions

- **Area:** the management pack in VCF Operations, its build and lab tools, and its side of two contracts: [C1, the KPI definitions](../glossary.md#c1), and [C2, the KPI metric keys](../glossary.md#c2), both described in [CONTRACTS.md](../../CONTRACTS.md).
- **Milestones** ([ROADMAP.md](../../ROADMAP.md)): R-ADP-005 to R-ADP-008, R-ADP-010, R-ADP-011 and R-ADP-025 belong to M2, and R-ADP-018 to R-ADP-023 to M3. R-ADP-019, R-ADP-020 and R-ADP-023 are needed before M6, the first live cluster in PCM. R-ADP-013 to R-ADP-017, the state codes, come after release 1.0 ([WD-033](../../DECISIONS.md)). R-ADP-007 is needed before M7, when PCM also reads hosts, VMs and vCenter. R-ADP-024 depends on the new lab repository [lab-build](https://github.com/e1-rahabok/lab-build) and comes after release 1.0 ([WD-031](../../DECISIONS.md)).
- **Keys** start with `vCommunity|` ([WD-032](../../DECISIONS.md)).
- **The adapter may change anything.** The author confirmed that no installed instance or upgrade path needs protecting: Q-I4 and Q-2 in [round 1](../interview-round-1.md), recorded as decisions [WD-007 and WD-016](../../DECISIONS.md).
- **How lab scenarios run.** From the author's laptop over VPN, with the repository's own tools ([tools/README.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/README.md)): [build.ps1](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/build/build.ps1), [install.ps1](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/install/install.ps1), [restart.ps1](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/restart/restart.ps1), then one collection cycle, then [validate.ps1](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.ps1). This sequence is called "install and validate" below. The live validation checks the build installed on the lab, so a lab scenario passes only after that build is installed ([validate.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.md#L12)).
- **Test names marked "(new)"** do not exist yet. Each is written as part of its requirement.

## Pack identity

### R-ADP-001 Dropped: the pack has its own identity in VCF Operations

Source: [WD-032](../../DECISIONS.md).

Dropped by WD-032: the pack keeps adapter kind `vCommunity`, display name "VCF vCommunity Adapter", manifest name `iSDK_vCommunity`, its image and its pak name.

### R-ADP-002 Dropped: every key has the new prefix, set in one place

Source: [WD-032](../../DECISIONS.md).

Dropped by WD-032: every key keeps the prefix `vCommunity|`.

### R-ADP-003 Dropped: the old pack is replaced on the lab

Source: [WD-032](../../DECISIONS.md).

Dropped by WD-032: with the identity kept, the pack is upgraded in place and keeps its history.

### R-ADP-004 Dropped: the shipped content uses the new keys and names

Source: [WD-032](../../DECISIONS.md).

Dropped by WD-032: the shipped content keeps its keys and its names, "vCommunity" included.

### R-ADP-005 No file names the old repository

Milestone: M2. The pack's own names, such as "vCommunity MP" and "vCommunity_", stay (WD-032).

Source: Q-3 in [round 1](../interview-round-1.md) ("agree": one pull request per repository, archive files left as they are); Q-80 in [round 2](../interview-round-2.md) (the dated engineering reviews and the README's sentence about the vCommunity keep the old name).

- Given the files git tracks in the PCM-Adapter repository, outside the dated engineering reviews
- When they are searched
- Then none contains "VCF-vCommunity-Adapter" or "private-cloud-management", the old names of two repositories
- And the README badges, the link in [resources.properties](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/resources/resources.properties#L7), the release command in [validate.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.md#L135) and the image path in [dark-site.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/installation-guide/dark-site.md#L48) and [system-requirements.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/installation-guide/system-requirements.md#L19) name VCF vCommunity Adapter

Test scenarios:
- T-ADP-005a (anywhere, automated by `Management Pack/tests/test_old_name.py` (new), run in CI like [test_docs_links.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/tests/test_docs_links.py)): run `git ls-files`, read each text file outside the archive, and search for the two old repository names; expect no match outside the engineering reviews.

### R-ADP-025 One name for the management pack

Milestone: M2.

Source: WD-030 (guessable names, one word per concept); WD-032 (the display name "VCF vCommunity Adapter" stays). An audit on 2026-11-27 found six names for the pack in the PCM-Adapter repository.

- Given the files git tracks in the PCM-Adapter repository, outside the dated engineering reviews
- When a file names the management pack
- Then it uses "VCF vCommunity Adapter", and "the adapter" only after that name in the same file
- And no file uses "vCommunity MP", "vCommunity Management Pack" or "the pack" for it
- And "PCM-Adapter" names only the repository
- And the copyright lines at the top of the code files stay as they are

Test scenarios:
- T-ADP-025a (anywhere, automated by `Management Pack/tests/test_old_name.py` (new), the test of T-ADP-005a): read each tracked text file outside the engineering reviews; skip each code file's copyright line and the author line under it; expect no "vCommunity MP", "vCommunity Management Pack" or "the pack".

## Metric keys and names

### R-ADP-006 A metric's label equals the Agent E2 catalog name

Milestone: M2.

Source: Q-1 in [round 1](../interview-round-1.md) ("For key, adapter is correct. For name, Agent E2 is correct."); Q-89 in [round 2](../interview-round-2.md) (a key column in every catalog row); Q-88 in [round 3](../interview-round-3.md) (the run queue is per vCPU); [WD-016](../../DECISIONS.md); [WD-001](../../DECISIONS.md), Agent E2 as the source of domain knowledge.

- Given a KPI row in any of the six KPI modules under [Management Pack/app/metrics](https://github.com/e1-rahabok/PCM-Adapter/tree/main/Management%20Pack/app/metrics)
- When the adapter definition is built
- Then the row's key is its adapter name, as today
- And its label, the name VCF Operations shows, is the catalog's metric name without its unit
- And this holds for the 11 VM Performance and Guest OS Performance rows that have no catalog label today, with the Guest OS run queue row named "Peak run queue length per vCPU" after agent-e2 renames it
- And the KPI definitions check matches adapter rows to catalog rows by key, using the catalog's key column
- And the known name gaps in [the KPI definitions check](../../checks/kpi_definitions.py#L62) (`NAME_GAPS`) are empty

Test scenarios:
- T-ADP-006a (anywhere, automated by [checks/kpi_definitions.py](../../checks/kpi_definitions.py) through `uv run checks/run_all.py`): with `NAME_GAPS` emptied; expect 0 differences for all six KPIs.
- T-ADP-006b (lab, automated by a new [screenshot.ps1](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/screenshot/screenshot.md) entry, reviewed by hand): install; open the metric tree of one lab cluster and one lab VM; expect the catalog names. **Verify on the lab:** the labels are declared on the adapter's own object type "Cluster Compute Resource" ([definition.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/definition.py#L310)), while the values land on the vCenter adapter's `ClusterComputeResource` ([collectClusterData.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/collectors/cluster/collectClusterData.py#L70)). Nothing yet shows that VCF Operations displays those labels on the vCenter objects.

### R-ADP-007 The declared keys equal the published keys

Milestone: M2.

Source: Q-29 in [round 1](../interview-round-1.md) (its recommendation: fix issue [#85](https://github.com/e1-rahabok/PCM-Adapter/issues/85) before PCM reads host, VM and vCenter keys; the answer does not change that).

- Given every object type the adapter publishes on: cluster, host, VM, datastore, vCenter, vSphere World, datacenter, and its own types
- When the adapter definition is compared with what the collectors publish
- Then each published key is declared, with the same groups and spelling
- And each declared key is published by some collector
- And the case in issue #85 is closed, including the cluster property declared as `Host Isolation` ([definition.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/definition.py#L336)) and published as `Response \ Host Isolation` ([ha_properties.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/properties/cluster/ha_properties.py#L12))

Test scenarios:
- T-ADP-007a (anywhere, automated by `Management Pack/tests/test_declared_keys.py` (new)): build the definition; run every collector against the fakes; expect the two key sets to be equal, for each object type.
- T-ADP-007b (lab, automated by a new validate.ps1 check): for one object of each type, read the `vCommunity|` keys from `GET /suite-api/api/resources/stats/latest?resourceId=<id>` and from `GET /suite-api/api/resources/<id>/properties`; expect each to be in the declared set. **Verify on the lab** that the properties endpoint returns the adapter's properties for a vCenter object.

### R-ADP-008 Each sub-metric reads the statistic its catalog name states

Milestone: M2.

Source: Q-19 in [round 1](../interview-round-1.md) ("20-second. If a metric does not have the word peak, it's likely a 5-minute average."); Q-81 in [round 2](../interview-round-2.md) (the catalog's interval is the rule); [WD-016](../../DECISIONS.md).

- Given a KPI row whose catalog limits are given for the `20s` interval, a 20-second peak
- When the adapter reads its input from VCF Operations
- Then it reads a 20-second peak stat, one whose key contains `20_sec_peak`
- And a row whose catalog limits are given for `5m` reads a 5-minute value
- And each `Metric` row in [kpi_score.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/kpi_score.py#L67) records its interval, `20s` or `5m`
- And the KPI definitions check compares that interval with the catalog interval whose limits matched

Test scenarios:
- T-ADP-008a (anywhere, automated by [checks/kpi_definitions.py](../../checks/kpi_definitions.py), extended): for each matched row, expect the adapter's interval to equal the catalog interval that holds the matching limits.
- T-ADP-008b (anywhere, automated by `Management Pack/tests/test_statistics.py` (new)): for every `20s` row, expect its stat key to contain `20_sec_peak`. Known cases, settled by Q-81 in round 2 (agent-e2 adds "peak" to the memory wait names; the dropped TX row is checked on the lab, and becomes 5-minute without "peak" if no 20-second peak exists): VM Network Dropped Tx reads `net|droppedTxPct_max` ([vm_performance_metrics.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/vm/vm_performance_metrics.py#L97)) against a catalog name with "peak" ([thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml#L60)). The memory wait rows read a 20-second peak ([memory_wait.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/vm/memory_wait.py#L25)), but their catalog names have no "peak" ([thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml#L39)).

## Scoring tables compared with the Agent E2 catalog

### R-ADP-009 Dropped: the scoring formula reproduces the catalog's worked examples

Source: WD-036.

Dropped by WD-036. The catalog holds no scoring rules or worked examples. The adapter's own tests ([test_kpi_score.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/tests/test_kpi_score.py)) cover its scoring code.

### R-ADP-010 The score bands equal the catalog's score rows

Milestone: M2.

Source: Q-15 in [round 1](../interview-round-1.md) ("All their logic should come from Agent E2. PCM Adapter must implement the same."); [WD-016](../../DECISIONS.md); WD-036.

- Given the catalog's score rows for Cluster Risk ([thresholds-risk.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-risk.yaml#L23)) and Cluster Consumption ([thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml#L40)), and a score row for Cluster Performance that agent-e2 adds first (the catalog has none today)
- When the adapter colours a KPI value, in `band()` of [periodic_cluster_check.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/periodic_cluster_check.py#L97)
- Then its band limits (25, 50 and 75 on the health scale today) equal the catalog's score limits for that KPI

Test scenarios:
- T-ADP-010a (anywhere, automated by [checks/kpi_definitions.py](../../checks/kpi_definitions.py), extended to the `score` sections): expect the adapter's `RED_BELOW`, `ORANGE_BELOW` and `YELLOW_BELOW` to equal each catalog score row, after the "higher is worse" flip. A KPI with no score row in the catalog fails.
- T-ADP-010b (anywhere, automated by the existing tests `test_bands` and `test_a_value_on_a_limit_belongs_to_the_better_band` in [test_periodic_cluster_check.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/tests/test_periodic_cluster_check.py#L84)): expect them to pass.

### R-ADP-011 The closure levels equal the catalog's

Milestone: M2.

Source: Q-15 and Q-16 in [round 1](../interview-round-1.md) (Q-16: "agree", one Cluster Risk level for every cluster); [WD-016](../../DECISIONS.md).

- Given the catalog's Close for Business decisions in [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml#L55)
- When the Periodic Cluster Check decides Close for Business
- Then Consumption closes above 80 (red) and above 60 (orange), Performance below 20 (red) and below 40 (orange), as in `CLOSE_RED_BELOW` and `CLOSE_ORANGE_BELOW` ([periodic_cluster_check.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/periodic_cluster_check.py#L104))
- And Risk decides above 60 for every cluster
- And Agent E2's catalog holds one Risk level for every cluster; that change to the catalog is made in agent-e2 (WD-001)
- And the default window, 24 hours with 5 % of the worst samples ignored, equals the catalog's "95th percentile of the last 24 hours" (5th percentile for Performance)

Test scenarios:
- T-ADP-011a (anywhere, automated by [checks/kpi_definitions.py](../../checks/kpi_definitions.py), extended to the `decisions` section): expect every closure level, and the default period and percent, to equal the catalog.
- T-ADP-011b (anywhere, automated by the existing tests from `test_closure_levels_sit_inside_the_display_bands` to `test_open_when_healthy` in [test_periodic_cluster_check.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/tests/test_periodic_cluster_check.py#L98)): expect them to pass.
- T-ADP-011c (lab, automated by validate.ps1 check 20): install and validate after a window has ended; expect the published Close for Business to follow the rule from the published Worst values on every sampled cluster.

### R-ADP-012 Dropped: usable capacity is Total − HA − Buffer

Source: WD-036.

Dropped by WD-036. The formula is domain knowledge in Agent E2, and the adapter's existing test `test_consumption_is_against_usable_capacity` covers its code. Closing issue [#14](https://github.com/e1-rahabok/PCM-Adapter/issues/14) is the adapter repository's own work.

## Explicit data states

The adapter today publishes nothing for a row with no data. A Suite API "latest" read then returns the last old value as if it were current ([metrics/README.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics/README.md#L138)). The author asked for this to be fixed in the adapter (Q-28), so that PCM shows what the adapter publishes and says "No data" when it is stale ([WD-015](../../DECISIONS.md)).

In release 1.0, only R-ADP-018 is built: a value from a partial read is not published. PCM shows "No data" for a stale value from the time of the value (R-LIVE-015 in [pcm-live.md](pcm-live.md)). The state codes below, which say why a row has no value, come after release 1.0 ([WD-033](../../DECISIONS.md)).

The states use one code each:

| Code | State | Applies to | Meaning |
|---|---|---|---|
| 0 | Counted | row, KPI | The value is published and counts in the KPI; for a KPI, the score is published |
| 1 | Excluded when green | row | The value is published, and left out of the KPI while green |
| 2 | Not applicable | row, KPI | The object has nothing to measure: no host with memory tiering, no powered-on VM, or no running host |
| 3 | Not collected | row | VCF Operations does not collect an input, for example a policy counter that is off |
| 4 | No current data | row, KPI | An input has no sample in the last 10 minutes ([ops_stats.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/utils/ops_stats.py#L32)); for a KPI, no row has data |
| 5 | Read failed | row, KPI | A stats request to VCF Operations failed, fully or for part of the objects |
| 6 | No usable capacity | row, KPI | Cluster Consumption only: HA and the buffer leave nothing for VMs; the KPI is 100 |

### R-ADP-013 Every row and every KPI has a state, every cycle

Milestone: after release 1.0 ([WD-033](../../DECISIONS.md)).

Source: Q-28 in [round 1](../interview-round-1.md) ("we should fix them in the PCM Adapter"); [WD-016](../../DECISIONS.md) ("Data absent by design is made explicit by the adapter"); Q-27 and [WD-015](../../DECISIONS.md) (PCM says "No data" when a value is stale).

- Given an object with a KPI: a cluster, host or VM
- When a collection cycle publishes that KPI
- Then for each row the adapter publishes `vCommunity|<KPI>|State|<row key>` with one code from the table
- And for the KPI it publishes `vCommunity|<KPI>|State|<KPI key>`
- And the states carry the same timestamp as the values of that cycle
- And a row's value is published exactly when its state is 0 or 1
- And the code table is in the adapter's [Metrics reference](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics/README.md) and in the C2 contract

Test scenarios:
- T-ADP-013a (anywhere, automated by `Management Pack/tests/test_data_states.py` (new)): for each of the six KPI modules, call its collect function with fakes for each state; expect one state per row and per KPI, a value exactly for states 0 and 1, and one timestamp for the cycle.
- T-ADP-013b (lab, automated by a new validate.ps1 check): install and validate; on every sampled cluster, host and VM, expect a state key for every row and KPI, no state older than the KPI's newest sample, and a value next to every state 0 or 1.

### R-ADP-014 Memory tiering rows say when a cluster has no tiering

Milestone: after release 1.0 ([WD-033](../../DECISIONS.md)).

Source: Q-28 and Q-38 in [round 1](../interview-round-1.md) (Q-38: "the physical host does not have memory tiering"); [WD-018](../../DECISIONS.md), the lab-build decision.

- Given a cluster where no host has an NVMe memory tier (`mem:NVMe|memory_tier_size` is 0 or missing)
- When Cluster Risk and Cluster Consumption are published
- Then Worst ESXi Active Memory, Worst ESXi Memory Tiering Latency, Cluster-wide ESXi DRAM Consumed and Cluster Memory Tiering Consumption have state 2
- And the same holds for the tiering row of ESXi Performance on such a host

Test scenarios:
- T-ADP-014a (anywhere, automated by `Management Pack/tests/test_data_states.py` (new)): hosts without the tier stat; expect state 2 on the four rows and no value.
- T-ADP-014b (lab, automated by the new validate.ps1 state check): install and validate; on every physical lab cluster, expect state 2 on the four rows.

### R-ADP-015 Bad network packets say when the policy counters are off

Milestone: after release 1.0 ([WD-033](../../DECISIONS.md)).

Source: Q-28 in [round 1](../interview-round-1.md); the policy page [policy.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/configuration-guide/policy.md#L7) (Total Packets Received and Transmitted are off by default).

- Given hosts that report the dropped and error packet counters, but not `net|packetsRx_summation_sum` and `net|packetsTx_summation_sum` ([host_bad_network_packets.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/host/host_bad_network_packets.py#L20))
- When Cluster Performance and ESXi Performance are published
- Then the bad packets row has state 3
- And when the two counters are on, the row has state 0 or 1

Test scenarios:
- T-ADP-015a (anywhere, automated by `Management Pack/tests/test_data_states.py` (new)): fake host stats with and without the two counters; expect state 3, then state 0 or 1.
- T-ADP-015b (lab, automated by the new validate.ps1 state check): with the lab policy as it is; expect state 3 if the counters are off. Then the counters are turned on (question 14); after one cycle, expect state 0 or 1. **Verify on the lab** that a counter turned off is absent from `stats/latest`, so that "off" can be told from "late".

### R-ADP-016 VM rows say when a cluster or host has no powered-on VM

Milestone: after release 1.0 ([WD-033](../../DECISIONS.md)).

Source: Q-28 in [round 1](../interview-round-1.md).

- Given a cluster or host with no powered-on VM
- When Cluster Performance or ESXi Performance is published
- Then the 8 VM contention rows have state 2
- And the KPI is scored from the rows that remain, with state 0, or has state 2 when none remains

Test scenarios:
- T-ADP-016a (anywhere, automated by `Management Pack/tests/test_data_states.py` (new)): a cluster whose VMs are all powered off; expect state 2 on the 8 rows.
- T-ADP-016b (lab, manual with the author, because it powers VMs off): on a lab host chosen by the author, with its VMs moved or powered off; expect state 2 on its ESXi Performance VM rows after one cycle.

### R-ADP-017 Cluster Consumption says when it is full or when no host runs

Milestone: after release 1.0 ([WD-033](../../DECISIONS.md)).

Source: Q-28 in [round 1](../interview-round-1.md); the two cases in [cluster_consumption_metrics.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/cluster_consumption_metrics.py#L336).

- Given a cluster whose hosts run, while HA and the buffer leave no usable capacity
- When Cluster Consumption is published
- Then the KPI is 100 with state 6, and the rows of that resource have state 6
- And given a cluster where no host runs (down, powered off, in maintenance mode or disconnected), the KPI and every row have state 2 and no value

Test scenarios:
- T-ADP-017a (anywhere, automated by `test_usable_zero_is_full_but_missing_usable_is_no_data` in [test_cluster_consumption_metrics.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/tests/test_cluster_consumption_metrics.py#L146), extended with the states): expect state 6, then state 2.
- T-ADP-017b (lab, manual with the author, because it puts hosts into maintenance mode): on a two-host cluster chosen by the author, with one host in maintenance mode and HA tolerating one failure; expect state 6 and a KPI of 100.

### R-ADP-018 A value built from a partial read is not published

Milestone: M3.

Source: Q-28 in [round 1](../interview-round-1.md) (its evidence names issue [#60](https://github.com/e1-rahabok/PCM-Adapter/issues/60): values from partial reads look normal); WD-033 (in release 1.0, without the state code).

- Given a stats request that fails for one batch of objects ([ops_stats.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/utils/ops_stats.py#L155): "resources have no stats this cycle")
- When a row aggregates over those objects, for example the worst VM of a cluster
- Then the row and its KPI are not published that cycle
- And the log names the KPI and the number of objects not read
- And issue #60 is closed

Test scenarios:
- T-ADP-018a (anywhere, automated by `Management Pack/tests/test_data_states.py` (new)): a fake Suite API that answers HTTP 500 to the second batch, with a small batch size; expect no value on every row and KPI built from that read, and one log line per KPI.

## Key list from the live environment

PCM must take the keys it reads from a live environment (Q-29). The adapter's part is to make the full key set visible on any one object, every cycle, so one read gives the list.

**How the keys are read today.** `GET /suite-api/api/resources?adapterKind=VMWARE&resourceKind=ClusterComputeResource` lists the clusters, then `GET /suite-api/api/resources/stats/latest?resourceId=<id>` returns every stat of one object, with `values[].stat-list.stat[].statKey.key`, `timestamps` and `data`. validate.ps1 does this ([validate.ps1](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.ps1#L142)) and keeps the keys that start with the prefix. The adapter itself uses `POST /suite-api/api/resources/stats/latest/query` with a list of resource IDs and stat keys ([ops_stats.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/utils/ops_stats.py#L16)). The Suite API returns keys only. The names come from the Agent E2 catalog (R-ADP-006). A row with no data is missing from that read, so the list depends on the object. In release 1.0 the expected set comes from the module tables (R-ADP-007), and the lab read checks that no other key appears ([WD-033](../../DECISIONS.md)).

Two other endpoints may give the declared keys with their names: `GET /suite-api/api/resources/<id>/statkeys` and `GET /suite-api/api/adapterkinds/vCommunity/resourcekinds/<kind>/statkeys`. Neither is used in the repository. **Verify on the lab** what each returns for a vCenter cluster.

### R-ADP-019 One read of one object gives its full key set

Source: Q-29 in [round 1](../interview-round-1.md) ("You will need to get from a live environment"); Q-1 (key from the adapter, name from the catalog); WD-033 (no state keys in release 1.0).

- Given one lab cluster, one host and one VM, after one collection cycle of the new pack
- When `GET /suite-api/api/resources/stats/latest?resourceId=<id>` is read for each, keeping the keys that start with `vCommunity|`
- Then every key found is in the expected set for its object type
- And the expected set for a cluster is the one listed in [Cluster keys](#cluster-keys) below
- And every expected key that no object of the type carries is listed, with the reason its row has no data

Test scenarios:
- T-ADP-019a (anywhere, automated by `Management Pack/tests/test_declared_keys.py` (new)): from the module tables (`GROUP`, `KPI_KEY`, `PUBLISHED_METRICS`), build the expected key set per object type; expect it to equal the keys the collectors publish with fakes.
- T-ADP-019b (lab, automated by a new validate.ps1 check that writes the keys it found to a file for PCM's key list): install and validate; for every sampled cluster, host and VM, expect no key outside the expected set, and a list of the expected keys not seen, each with its reason (for example no memory tiering, packet counters off).

## Periodic Cluster Check settings

The author asked how PCM gets the check's settings (Q-31).

**How they are read today.** The settings are Advanced Settings of each VCF vCommunity Adapter instance, and are not published on the cluster ([periodic-cluster-check.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics/periodic-cluster-check.md#L46)). `GET /suite-api/api/adapters?adapterKindKey=vCommunity` returns `adapterInstancesInfoDto[]`. Each instance has `resourceKey.resourceIdentifiers[]`, a list of `identifierType.name` and `value` pairs:

- `cluster_check_period_hours`: stored zero-padded, "01" to "24" ([periodic_cluster_check.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/periodic_cluster_check.py#L61))
- `periodic_cluster_check_time`: "HH:MM" in UTC
- `cluster_check_worst_percent`: 0 to 50
- `host`: the vCenter the instance collects

An empty value means the default: 24 hours, 00:00 and 5 %. validate.ps1 reads them this way ([validate.ps1](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.ps1#L115) and [L270](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.ps1#L270)). It takes the first instance's values for every cluster, which is wrong when two instances differ.

Linking a cluster to its instance takes three more steps:

1. Match the instance's `host` to the `VCURL` identifier of a VMware vCenter adapter instance ([adapter.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/adapter.py#L406)).
2. Find that instance's ID through `GET /suite-api/api/adapters?adapterKindKey=VMWARE`.
3. Query the clusters with that `adapterInstanceId` ([collectClusterData.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/collectors/cluster/collectClusterData.py#L70)).

**Verify on the lab** that a read-only account may call `GET /api/adapters`. Because this path is long, R-ADP-020 publishes the settings on each cluster.

### R-ADP-020 Each cluster carries its check settings and each result its window

Source: Q-31 in [round 1](../interview-round-1.md) ("PCM gets from the PCM Adapter"); [WD-015](../../DECISIONS.md) (PCM shows what the VCF vCommunity Adapter publishes).

- Given a cluster collected by a VCF vCommunity Adapter instance
- When a collection cycle runs
- Then the cluster has the properties `vCommunity|Periodic Cluster Check|Period (hours)`, `vCommunity|Periodic Cluster Check|Time (UTC)` and `vCommunity|Periodic Cluster Check|Worst Percent`, with the values the check uses after defaults
- And each time the check publishes its four values, it also publishes the metric `vCommunity|Periodic Cluster Check|Window End`, the end of the window in UTC as epoch milliseconds, with the same timestamp
- And PCM can read both with the cluster, through `GET /suite-api/api/resources/<id>/properties` and `stats/latest`, with no read of the adapter instances

Test scenarios:
- T-ADP-020a (anywhere, automated by [test_periodic_cluster_check.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/tests/test_periodic_cluster_check.py), extended from `test_publish`): with set and empty settings; expect the three properties with the values in use, and Window End equal to the window the values cover.
- T-ADP-020b (lab, automated by validate.ps1 check 19, changed to read Window End and the properties of each cluster): install and validate after a window ends; expect each sampled cluster's properties to match its instance's Advanced Settings, and Window End to equal the latest window end.

## Credentials for the lab tools

### R-ADP-021 Reading and validating use a read-only account

Source: Q-40 in [round 1](../interview-round-1.md) ("agree": two DPAPI files in `$HOME\.secrets\`); [WD-011](../../DECISIONS.md), the decision on lab credentials.

- Given the author's laptop, with the read-only VCF Operations login saved as a DPAPI file in `$HOME\.secrets\` (`Export-Clixml`, the format in [validate.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.md#L24): `Url` and `Credential`)
- When validate.ps1 or screenshot.ps1 runs with no `-SecretFile`
- Then it reads that file
- And no script reads `.secrets` inside the repository folder, as all four do today ([validate.ps1](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.ps1#L32))
- And [tools/README.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/README.md#L51), [validate.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.md#L24) and [CLAUDE.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/CLAUDE.md#L53) describe the two files

Test scenarios:
- T-ADP-021a (anywhere, automated by `Management Pack/tests/test_tool_secrets.py` (new)): read the `param` blocks of the four scripts; expect each default `-SecretFile` under `$HOME\.secrets\`, and the read-only file for validate.ps1 and screenshot.ps1.
- T-ADP-021b (lab, automated by validate.ps1): run it with the read-only file; expect exit 0 and every check that passes with the admin login to pass. **Verify on the lab** that the read-only account can read adapters, solutions and resources, and can open the pages screenshot.ps1 takes.

### R-ADP-022 Installing and restarting use the admin account

Source: Q-40 in [round 1](../interview-round-1.md); [WD-011](../../DECISIONS.md).

- Given the admin login saved as a second DPAPI file in `$HOME\.secrets\`
- When install.ps1 or restart.ps1 runs with no `-SecretFile`
- Then it reads the admin file
- And when it is given the read-only file, it stops with a message naming the admin file, before it uploads or stops anything

Test scenarios:
- T-ADP-022a (anywhere, automated by `Management Pack/tests/test_tool_secrets.py` (new)): expect the admin file as the default of install.ps1 and restart.ps1.
- T-ADP-022b (lab, automated by the install and validate sequence): install.ps1 and restart.ps1 with the admin file, then validate.ps1 with the read-only file; expect all three to pass.
- T-ADP-022c (lab, run once by hand): restart.ps1 with the read-only file; expect it to stop with the message and every Adapter Instance still collecting.

## Live checks and the tiering lab

### R-ADP-023 The inputs not yet seen live are checked on the lab

Source: Q-38 in [round 1](../interview-round-1.md) (lab facts to confirm before M6); issue [#2](https://github.com/e1-rahabok/PCM-Adapter/issues/2) ("Verify on a live system"); [WD-018](../../DECISIONS.md).

- Given the lab VCF Operations
- When a read-only script reads the lab hosts and VMs
- Then the values of `runtime|powerState` and `runtime|maintenanceState` that the adapter compares against are recorded for a powered-on host and a host in maintenance mode ([cluster_consumption_metrics.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/cluster_consumption_metrics.py#L73))
- And the VCF Operations version is recorded in the workspace [SYSTEM.md](../../SYSTEM.md)
- And issue #2 is brought up to date: it still names the old Daily Cluster Check

Test scenarios:
- T-ADP-023a (lab, automated by a new read-only option of validate.ps1, with one manual step): the author puts one host into maintenance mode; the script reads both properties on every host; expect values that the adapter's comparison, with case and spaces ignored, classifies as the code expects.

### R-ADP-024 Memory tiering is tested on nested hosts built by lab-build

Source: Q-38 in [round 1](../interview-round-1.md) ("Create the automatic build https://github.com/e1-rahabok/lab-build using Virtual ESXi"); [WD-018](../../DECISIONS.md); requirements in [lab-build.md](lab-build.md).

Depends on lab-build: a cluster of nested ESXi hosts with an NVMe memory tier, monitored by the lab VCF Operations.

- Given that cluster, after one collection cycle of the new pack
- When the tiering rows are read
- Then Worst ESXi Active Memory, Worst ESXi Memory Tiering Latency, Cluster-wide ESXi DRAM Consumed and Cluster Memory Tiering Consumption have state 0 or 1 with a value
- And the inputs marked "not checked on a live host yet" have values: `mem|active_average` ([cluster_risk_metrics.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/cluster_risk_metrics.py#L212)) and `mem:NVMe|bandwidth.read_latest` ([memory_wait.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/vm/memory_wait.py#L26))
- And Memory Wait on a VM that reads from the tier is higher than its Memory Contention

Test scenarios:
- T-ADP-024a (lab, automated by the new validate.ps1 state check, pointed at the lab-build cluster): expect the four rows with state 0 or 1 and a value, and the two inputs present in `stats/latest`.
- T-ADP-024b (lab, automated by a lab-build load step, then validate.ps1): a VM on a tiered host whose memory exceeds the DRAM it may use; expect its VM Performance memory wait above its `mem|20_sec_peak_host_contentionPct`.

## Cluster keys

The value keys a cluster carries. After release 1.0, each row also gets a state key, `vCommunity|<KPI>|State|<row key>`, and each KPI a state key, `vCommunity|<KPI>|State|<KPI key>` (R-ADP-013). The keys after the prefix are the adapter's row names today.

| KPI | KPI key | Row keys | Defined in |
|---|---|---|---|
| Cluster Performance | `vCommunity\|Cluster Performance\|Cluster Performance Score` | Worst VM CPU Ready, Worst VM CPU Co-Stop, Worst VM Memory Latency, Worst VM Disk Latency, 90th Percentile VM CPU Ready, 90th Percentile VM CPU Co-Stop, 90th Percentile VM Memory Latency, 90th Percentile VM Disk Latency, Highest ESXi Bad Network Packets | [cluster_performance_metrics.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/cluster_performance_metrics.py#L28), [contention_by_vms.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/vm/contention_by_vms.py#L47) |
| Cluster Risk | `vCommunity\|Cluster Risk\|Cluster Risk Score` | Highest ESXi CPU Thread Utilization, Worst ESXi CPU Imbalance, Worst ESXi Memory Ballooned, Worst ESXi Memory Zip Swap, Worst ESXi Active Memory, Worst ESXi Memory Tiering Latency, Highest ESXi CPU Reservation, Highest ESXi Memory Reservation, Highest ESXi CPU Overcommit Ratio, Highest ESXi Memory Overcommit Ratio, Highest CPU Monster VM to Host Ratio, Highest Memory Monster VM to Host Ratio | [cluster_risk_metrics.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/cluster_risk_metrics.py#L349) |
| Cluster Consumption | `vCommunity\|Cluster Consumption\|Cluster Consumption Score` | Cluster-wide ESXi CPU Thread Utilization, Cluster-wide ESXi Memory Consumed, Cluster-wide ESXi DRAM Consumed, Cluster Memory Tiering Consumption, Cluster-wide ESXi Memory Ballooned, Cluster-wide ESXi Memory Zip Swap | [cluster_consumption_metrics.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/cluster_consumption_metrics.py#L284) |
| Periodic Cluster Check | none | Worst Cluster Performance, Worst Cluster Risk, Worst Cluster Consumption, Close for Business, Window End (new, R-ADP-020) | [periodic_cluster_check.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/periodic_cluster_check.py#L81) |

## Questions for round two

The questions on this file, with their decisions, are in the [interview, round 2](../interview-round-2.md): Q-72 to Q-89. The few still open are in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md).
