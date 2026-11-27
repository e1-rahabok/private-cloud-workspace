# Requirements: PCM live demo

PCM's live demo is the L2 workspace reading the author's lab VCF Operations (https://10.115.1.81) through its Suite API. It is a separate demo with its own entry in the demo drop-down. The synthetic ACME demo stays as it is. The scope is performance and capacity management only. These requirements come from [W-015, the live demo decision](../../DECISIONS.md), and from the author's answers to Q-20 to Q-39 in the [interview, round 1](../interview-round-1.md) (also in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md) until they move). Other short names are explained in the [glossary](../glossary.md).

Milestones ([ROADMAP.md](../../ROADMAP.md)): M6 is one lab cluster's Cluster Performance on the L2 Performance tab; M7 is the rest of the live demo. Each requirement names its milestone.

Files involved:

- PCM's L2 specification: [spec/catalog/l2.yaml](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/catalog/l2.yaml), [spec/workspaces/l2/monitor.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/workspaces/l2/monitor.md), [spec/workspaces/l2/frame.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/workspaces/l2/frame.md), [spec/api/l2.yaml](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/api/l2.yaml).
- What PCM-Adapter publishes, and how it makes absent data and its check settings readable: [pcm-adapter.md](pcm-adapter.md), drafted in parallel. This file does not repeat it.
- The contracts: [C2, KPI metric keys](../glossary.md#c2) (the keys PCM-Adapter publishes and PCM reads) and [C3, the Agent E2 API](../glossary.md#c3) (the calls PCM makes to Agent E2), in [CONTRACTS.md](../../CONTRACTS.md).

Tests named below do not exist yet unless stated; "to write" marks them. Lab scenarios run from the author's laptop over the VPN. They use the read-only VCF Operations credential in `$HOME\.secrets\` ([W-011, lab credentials](../../DECISIONS.md)). They start by running PCM-Adapter's [validate.ps1](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.ps1), so a failure caused by a pack that is not collecting is reported as such. A lab scenario that cannot reach the lab is reported as not run, never as passed.

## The demo and its scope

### R-LIVE-001 A separate entry for the live demo

Source: the author's answers to Q-20 and Q-32 in the interview, round 1 ("The synthetic and the live are 2 separate demoes. Not flippable"); W-003, the decision to keep ACME and add a separate live demo.

Milestone: M6.

Given PCM runs with the demo control on
When a person opens the demo drop-down on any page
Then it lists one new entry for the live L2 demo, with its own URL (proposed: `/live/l2`)
And every synthetic entry keeps its place, its URL and its behaviour
And no page of either demo has a control that switches its data to the other

Test scenarios:
- T-LIVE-001a (anywhere, automated by build/tests/live.page.test.mjs::test_demo_entry, to write). Data: PCM started against the fake Suite API (build/tests/fake_suite_api.py, to write). Steps: open `/exec`, open the drop-down, choose the live entry. Expected: the entry is listed once; choosing it opens `/live/l2`; the synthetic entries are unchanged in order and URL.
- T-LIVE-001b (lab, automated by build/tests/live.lab.test.mjs::test_demo_entry, to write). Data: PCM on the lab VM (https://10.114.1.29) with the live connection configured. Steps: as in 001a. Expected: the live L2 page opens and its tree shows objects from the lab VCF Operations; a screenshot is saved for review.

### R-LIVE-002 Live and synthetic data never meet

Source: answer to Q-32; W-015.

Given the live demo and the synthetic demo run in the same PCM
When any page or API call of either demo answers
Then every value from the live demo carries the source of the lab VCF Operations instance in its metadata
And no live response contains a synthetic object, value, story or calendar entry
And no synthetic response contains a live object or value

Test scenarios:
- T-LIVE-002a (anywhere, automated by build/tests/test_live.py::test_no_mixing, to write). Data: the fake Suite API with three objects whose names do not occur in ACME. Steps: call every live API path, then every synthetic API path. Expected: live responses carry only the fake's objects, each value with the live source; synthetic responses carry no fake object name.

### R-LIVE-003 The live demo is the L2 workspace only

Source: answer to Q-22 ("The live mode is only L2. The rest of the role is synthetic only"); W-015.

Given the live demo
When a person or a test asks for an Executive, NOC, Capacity or Docs page or API path under the live prefix
Then PCM answers 404
And the live demo's pages link to no page of another workspace

Test scenarios:
- T-LIVE-003a (anywhere, automated by build/tests/test_live.py::test_l2_only, to write). Steps: request `/live/exec`, `/live/noc`, `/live/capacity`, `/live/docs` and their API paths. Expected: 404 for each; the live L2 page has no link to another workspace.

### R-LIVE-004 Performance and capacity only

Source: answer to Q-33 ("All these are out of scope in 1.0. Focus on performance and capacity management"); W-015.

Given the live L2 page
When it opens on any object
Then it shows the Monitor activity with the Performance and Capacity tabs only
And it shows no Troubleshoot, Improve, Rules or Calendar entry, no other pillar tab, no story, no case and no action button
And the live API refuses every write path with 404

Test scenarios:
- T-LIVE-004a (anywhere, automated by build/tests/live.page.test.mjs::test_tabs_only, to write). Data: the fake Suite API. Steps: open a cluster, a host and a VM. Expected: only Performance and Capacity tabs; no Troubleshoot, Improve, Rules or Calendar entry; no action button.
- T-LIVE-004b (anywhere, automated by build/tests/test_live.py::test_no_writes, to write). Steps: POST to each L2 write path under the live prefix (cases, proposals, decisions, policies, thresholds, calendar). Expected: 404 for each, and nothing written to PCM's database.

### R-LIVE-005 No clock and no planted stories in the live demo

Source: answer to Q-32; answer to Q-33.

Given the live API
When a request carries `now` or `enable`
Then PCM answers 400 and names the parameter
And the live page has no control that sets the clock or turns on a story

Test scenarios:
- T-LIVE-005a (anywhere, automated by build/tests/test_live.py::test_now_enable_refused, to write). Steps: call a live API path with `now=2026-10-19T10:05:00+08:00`, then with `enable=E-7`. Expected: 400 each time, with the parameter named in the body.

### R-LIVE-006 No class of service, region, environment or time zone

Source: answer to Q-24 ("All these are only applicable in synthetic"); W-015.

Given the live L2 page above the cluster, on the Performance or Capacity tab
When it opens
Then it has no class of service filter, and no text about Gold, Silver or Bronze
And the lines across clusters (worst and percentile) cover every cluster under the selected object
And no live object shows a region, location, class, environment or local time zone
And times are shown in the viewer's time zone with the zone named, as in the synthetic demo ([PCM D-074, three rules from the first build's review](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L81))

Test scenarios:
- T-LIVE-006a (anywhere, automated by build/tests/live.page.test.mjs::test_no_class, to write). Data: the fake Suite API with two clusters under one VCF instance. Steps: open the VCF instance's Performance and Capacity tabs. Expected: no class filter; the words Gold, Silver and Bronze are absent; the worst line is the lower of the two clusters at each point.

## Connection to VCF Operations

### R-LIVE-007 Sign-in with a read-only account from the lab VM's secret file

Source: answer to Q-34 ("agree"); W-011.

Given `/etc/pcm/pcm.env` on the lab VM holds the Suite API URL, user and password (proposed names `PCM_VCFOPS_URL`, `PCM_VCFOPS_USER`, `PCM_VCFOPS_PASSWORD`)
When the live demo needs data
Then PCM acquires a Suite API token with them, keeps it until it expires, and acquires a new one once after a 401
And the password and the token appear in no log, page, API response, error message or Agent E2 fact
And PCM itself keeps no sign-in of its own in release 1.0, behind the lab firewall

Test scenarios:
- T-LIVE-007a (anywhere, automated by build/tests/test_live.py::test_token_reuse_and_renewal, to write). Data: the fake Suite API counting token requests, set to answer 401 once. Steps: load three pages; then trigger the 401. Expected: one token request for the three pages; exactly one new token request after the 401; the page then loads.
- T-LIVE-007b (anywhere, automated by build/tests/test_live.py::test_no_secret_leak, to write). Data: a password and a token with a unique marker string. Steps: load every live page, force a login failure, and capture the server log, the responses and the facts sent to a stub Agent E2. Expected: the marker appears nowhere.
- T-LIVE-007c (lab, automated by tools/lab/Test-Live.ps1, to write). Data: the read-only credential. Steps: open the live page on the lab VM. Expected: data loads; the VCF Operations account used is the read-only one.

### R-LIVE-008 The lab certificate is checked

Source: answer to Q-34 (the lab CA pinned, no skip-verify).

Given the CA file of the lab VCF Operations certificate is named in `/etc/pcm/pcm.env` (proposed `PCM_VCFOPS_CA_FILE`)
When PCM connects to the Suite API
Then it verifies the certificate against that file
And a certificate that does not verify is a failed read (R-LIVE-011), with the reason "certificate not trusted"

Test scenarios:
- T-LIVE-008a (anywhere, automated by build/tests/test_live.py::test_tls_pinned, to write). Data: the fake Suite API over TLS with a certificate from a test CA. Steps: start PCM with the test CA, then with another CA. Expected: data loads with the right CA; with the wrong CA the page shows the failed-read state with "certificate not trusted".
- T-LIVE-008b (lab, automated by tools/lab/Test-Live.ps1, to write). Steps: read one cluster with the lab CA file. Expected: the read succeeds with verification on.

### R-LIVE-009 PCM never writes to VCF Operations

Source: answer to Q-23 ("It can't store in the VCF Operations database"); W-015.

Given the live demo
When PCM calls the Suite API for any page or Agent E2 question
Then every call is on a list of read calls: token acquire and release, GET calls, and the query calls that use POST only to read (for example the stats query)
And no call creates, changes or deletes anything in VCF Operations

Test scenarios:
- T-LIVE-009a (anywhere, automated by build/tests/test_live.py::test_read_calls_only, to write). Data: the fake Suite API logging method and path. Steps: load every live page and ask one Agent E2 question on each. Expected: every logged call is on the read list.
- T-LIVE-009b (lab, automated by tools/lab/Test-Live.ps1, to write). Steps: run the full lab test with the read-only account. Expected: no call is refused for lack of rights; the run passes.

### R-LIVE-010 Read through, with a 60-second cache and no store

Source: answer to Q-30 ("Agree"); W-015.

Given the live demo
When the same data is asked for twice within 60 seconds
Then PCM calls the Suite API once
And after 60 seconds it calls again
And PCM writes no metric value to its database, to disk or to any other store

Test scenarios:
- T-LIVE-010a (anywhere, automated by build/tests/test_live.py::test_cache_60s, to write). Data: the fake Suite API counting stats calls, and a fake clock in the cache. Steps: load a cluster's Performance tab at 0 s, 30 s and 61 s. Expected: two stats calls.
- T-LIVE-010b (anywhere, automated by build/tests/test_live.py::test_no_metric_store, to write). Steps: load every live page, then read PCM's SQLite file and its data folder. Expected: no metric value from the fake is stored anywhere.

### R-LIVE-011 A failed read shows "No data" for the whole page

Source: answer to Q-27 ("If the data is stale, say no data"); [PCM D-041, wall behaviour: stale data turns grey, never green](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L47).

Given the Suite API times out (proposed limit 10 seconds), answers an HTTP error, refuses the login, or fails the certificate check
When a live page loads
Then every KPI, part and check value on it shows "No data", in grey
And the page says that VCF Operations did not answer, with the reason and the time of the last good read
And no last value, zero or green colour is shown

Test scenarios:
- T-LIVE-011a (anywhere, automated by build/tests/live.page.test.mjs::test_failed_read, to write). Data: the fake Suite API set in turn to time out, answer 500, and refuse the login. Steps: load a cluster's Performance tab in each case. Expected: "No data" in grey for every figure; the reason and the last good read time are shown; no green and no 0.

## Inventory

### R-LIVE-012 The tree is VCF Operations' inventory, from the VCF instance down

Source: answer to Q-25 ("Use the inventory from VCF Operations. It starts with VCF Instance"); W-015.

Given the lab VCF Operations
When the live L2 page opens
Then its tree starts at the VCF instance objects and follows VCF Operations' own parent and child relationships down to the cluster, the ESXi host and the VM
And each node shows the object's name as VCF Operations shows it, and its type
And a node whose KPI has no data shows grey "No data"

Test scenarios:
- T-LIVE-012a (anywhere, automated by build/tests/test_live.py::test_tree_from_relationships, to write). Data: the fake Suite API with one VCF instance, two clusters, three hosts and five VMs, linked as parent and child. Steps: open the tree and expand every node. Expected: the same hierarchy, names and types as the fake; nothing else.
- T-LIVE-012b (lab, automated by tools/lab/live_reference.py and build/tests/live.lab.test.mjs::test_tree, to write). Steps: the reference script lists the lab's VCF instance and its descendants through the Suite API; the page test expands the tree. Expected: the tree has the same objects under the same parents; a screenshot is saved.

### R-LIVE-013 An object's ID is its VCF Operations resource ID

Source: answer to Q-26 ("Yes"); W-015.

Given any live object
When it appears in a URL, an API response or an Agent E2 fact
Then its ID is its VCF Operations resource ID, and its name is a separate field
And a renamed object keeps its URL

Test scenarios:
- T-LIVE-013a (anywhere, automated by build/tests/test_live.py::test_resource_id, to write). Data: the fake Suite API with two clusters of the same name under different vCenters. Steps: open each; then rename one in the fake. Expected: two distinct URLs by resource ID; after the rename the same URL opens the object with its new name.

## The values shown

### R-LIVE-014 PCM shows what PCM-Adapter publishes

Source: answer to Q-23 ("PCM can compute for UI purpose"); answer to Q-27 ("PCM simply regurgitate the adapter"); W-015.

Given a KPI, a part or a check value that PCM-Adapter publishes on a live object
When a live page shows it
Then each point on the chart is the sample value VCF Operations returns for that key and time
And PCM computes only what the page displays from those samples: Now, Worst, the percentile figure, the worst and percentile lines across objects, and the band colour
And PCM never recomputes a KPI from its parts, nor a check result from its inputs

Test scenarios:
- T-LIVE-014a (anywhere, automated by build/tests/test_live.py::test_values_passed_through, to write). Data: the fake Suite API with a Cluster Performance series that cannot be rebuilt from its parts. Steps: open the cluster's Performance tab. Expected: the chart's points equal the fake's KPI samples exactly.

### R-LIVE-015 A stale value shows "No data" at once

Source: answer to Q-27 ("No need to wait 15 minutes"); W-015. The rule below is proposed and waits for the author's confirmation in round two (Q-64 in the [interview, round 2](../interview-round-2.md): decided, 10 minutes).

Given PCM-Adapter collects every 5 minutes, and marks its own inputs stale after 10 minutes ([STALE_AFTER_MINUTES in ops_stats.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/utils/ops_stats.py#L32))
When the newest sample of a key on an object is older than 10 minutes (one collection cycle plus a margin of one cycle) at the time PCM reads it
Then Now shows "No data" in grey, with the time of the newest sample
And the chart keeps the older points and draws nothing after the newest
And the value is never shown as 0 or coloured green
And with the 60-second cache (R-LIVE-010), a value is shown as stale at most 11 minutes after its newest sample

Test scenarios:
- T-LIVE-015a (anywhere, automated by build/tests/test_live.py::test_stale_after_10_minutes, to write). Data: the fake Suite API with Cluster Performance samples ending 9 minutes ago on one cluster and 11 minutes ago on another. Steps: open both Performance tabs. Expected: the first shows its Now value; the second shows "No data" with the time of its newest sample.
- T-LIVE-015b (lab, automated by tools/lab/Test-Live.ps1, to write). Data: a powered-off lab VM, which PCM-Adapter stops publishing for. Steps: open the VM's Performance tab. Expected: VM Performance's Now shows "No data" with the time of the last sample. If the lab has no powered-off VM, the scenario reports "not run" and asks the author for one; it never changes the lab itself.

### R-LIVE-016 Gaps stay visible

Source: answer to Q-27; answer to Q-30.

Given a key whose samples in the window have a gap longer than one collection cycle
When its chart is drawn
Then the line breaks at the gap; nothing is drawn or filled in across it
And the percentile figure is computed over the samples that exist, and the page states how many

Test scenarios:
- T-LIVE-016a (anywhere, automated by build/tests/live.page.test.mjs::test_gap, to write). Data: the fake Suite API with a 24-hour series missing 40 minutes in the middle. Steps: open the chart. Expected: two separate line segments; the percentile uses 280 samples and says so.

### R-LIVE-017 A window longer than the history

Source: answer to Q-30 ("Agree": longer windows ask for the maximum per slot, draw nothing before the first point, say "Data from {date}").

Given a window of 7 days, 30 days or 1 year
When PCM reads a key for it
Then it asks VCF Operations for the maximum of each slot (1 hour, 4 hours and 1 day, as in [l2.statistics](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/catalog/l2.yaml#L241))
And when the key's history starts inside the window, nothing is drawn before the first point, and the chart says "Data from {date}"

Test scenarios:
- T-LIVE-017a (anywhere, automated by build/tests/test_live.py::test_long_window, to write). Data: the fake Suite API with 3 days of samples. Steps: open the 30-day window. Expected: the stats request asks for the maximum per 4-hour slot; the chart starts at the first point and says "Data from" that date.
- T-LIVE-017b (lab, automated by tools/lab/live_reference.py and build/tests/live.lab.test.mjs::test_long_window, to write). Steps: open one lab cluster's 7-day window; the reference script reads the same key with the maximum per hour. Expected: the points match at whole percent.

### R-LIVE-018 Parts carry the catalog's names, found by key

Source: answer to Q-1 ("For key, adapter is correct. For name, Agent E2 is correct"); [W-016, PCM-Adapter changes and key and name ownership](../../DECISIONS.md).

Given a part PCM-Adapter publishes under its key
When a live page shows it
Then its name is the name in Agent E2's catalog row that holds that key ([C1, KPI definitions](../glossary.md#c1))
And a key with no catalog row is shown under its key, and the key list check (R-LIVE-023) fails on it

Test scenarios:
- T-LIVE-018a (anywhere, automated by build/tests/test_live.py::test_part_names_from_catalog, to write). Data: the fake Suite API publishing two catalog keys and one key the catalog lacks. Steps: open the Details fold. Expected: the two parts under their catalog names; the third under its key.
- T-LIVE-018b (lab, automated by build/tests/live.lab.test.mjs::test_part_names, to write). Steps: open one lab cluster's Details folds. Expected: every part has its catalog name; a screenshot is saved.

### R-LIVE-019 Band colours follow the statistic of each key

Source: answer to Q-19 ("If a metric does not have the word peak, it's likely a 5-minute average"); W-016.

Given a part whose catalog name contains "peak"
When its figures and chart are coloured
Then the catalog's 20-second limits are used
And a part without "peak" uses the catalog's 5-minute limits
And a part with no limits for its statistic stays uncoloured

Test scenarios:
- T-LIVE-019a (anywhere, automated by build/tests/test_live.py::test_band_by_statistic, to write). Data: one peak part, one 5-minute part and one part with no 5-minute limits, from a copy of the catalog. Steps: open the Details fold. Expected: the first two coloured by the matching limits; the third plain.

### R-LIVE-020 Parts an object does not have

Source: answer to Q-28 ("we should fix them in the PCM Adapter"); W-016. Until PCM-Adapter makes absent data explicit ([pcm-adapter.md](pcm-adapter.md)), the rule below is proposed for round two.

Given a part key that VCF Operations does not hold for an object at all (for example a memory tiering key on a cluster without a tiered host)
When the object's Details fold opens
Then that part is left out, and the fold's heading counts the parts it shows
And a part key the object holds, with no recent sample, shows "No data" (R-LIVE-015)

Test scenarios:
- T-LIVE-020a (anywhere, automated by build/tests/test_live.py::test_absent_part, to write). Data: the fake Suite API with a cluster that holds 10 of the 12 Cluster Risk part keys, one of them with samples ending 30 minutes ago. Steps: open the Cluster Risk Details fold. Expected: 10 parts shown; the old one shows "No data".
- T-LIVE-020b (lab, automated by build/tests/live.lab.test.mjs::test_tiered_parts, to write). Data: the nested tiered cluster of [R-LAB-002](lab-build.md). Steps: open its Cluster Risk Details fold. Expected: the tiering parts are shown with data. Runs once the lab build exists; until then it reports "not run".

### R-LIVE-021 The Periodic Cluster Check as the adapter publishes it

Source: answer to Q-31 ("PCM gets from the PCM Adapter"); [PCM D-094, the Capacity tab reads the check and never recomputes it](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L101).

Given a lab cluster with Periodic Cluster Check values for its latest window
When its Capacity tab opens
Then the verdict and the three check values are the published values of that window, with its window end
And the rule shown is named by comparing published values with published closure levels; PCM decides nothing
And when no value is published for a window that ended more than 30 minutes ago (proposed: PCM-Adapter may publish a few cycles late), the page says "No check for the {period} to {end time}", never "Open"

Test scenarios:
- T-LIVE-021a (anywhere, automated by build/tests/test_live.py::test_check_published, to write). Data: the fake Suite API with a check window ending 2 hours ago (Close for Business 1) and none for a window ending 40 minutes ago. Steps: open the Capacity tab. Expected: "No check" for the latest window; the strip shows the earlier window closed with its published values.
- T-LIVE-021b (lab, automated by tools/lab/live_reference.py and build/tests/live.lab.test.mjs::test_check, to write). Steps: read the four check keys of one lab cluster through the Suite API; open its Capacity tab. Expected: the same verdict and values, with the same window end.

### R-LIVE-022 The check labels use the adapter's own settings

Source: answer to Q-31; [PCM D-095, which statistic, on which axis](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L102).

Given the Adapter Instance's Cluster Check Period, Cluster Check Time (UTC) and Cluster Check Worst Percent, made readable by PCM-Adapter ([pcm-adapter.md](pcm-adapter.md))
When the Capacity tab labels a check value
Then the label uses those settings, for example "5th percentile, 24 hours to 08:00 GMT+8"
And when the settings cannot be read, the label omits the percentile rank and the period, and says "check settings not available"

Test scenarios:
- T-LIVE-022a (anywhere, automated by build/tests/test_live.py::test_check_labels, to write). Data: the fake with period 12 hours, time 06:00 UTC and Worst Percent 10; then the fake with no settings. Steps: open the Capacity tab, viewer zone GMT+8. Expected: "10th percentile, 12 hours to 14:00 GMT+8" for Cluster Performance; then "check settings not available".
- T-LIVE-022b (lab, automated by tools/lab/Test-Live.ps1, to write). Steps: read the lab Adapter Instance's settings through the mechanism of pcm-adapter.md; open one cluster's Capacity tab. Expected: the labels match the settings.

### R-LIVE-023 The key list comes from the live environment

Source: answer to Q-29 ("You will need to get from a live environment"); C2.

Given the lab VCF Operations with PCM-Adapter installed
When a read-only tool lists the `vCommunity|` keys, and the VCF Operations capacity keys PCM reads, that the cluster, host and VM objects hold
Then it writes one file in PCM's specification (proposed `spec/catalog/vcf-operations-keys.yaml`) with each key, its object type, its unit and its catalog name, plus the adapter version and the date
And every key PCM's live demo reads is in that file
And the C2 check compares the file with the keys PCM reads and with what PCM-Adapter says it publishes ([pcm-adapter.md](pcm-adapter.md))

Test scenarios:
- T-LIVE-023a (lab, automated by tools/lab/live_keys.py, to write). Steps: run the tool against the lab. Expected: the file lists at least the KPI score keys and their parts for cluster, host and VM; it names the adapter version shown by validate.ps1.
- T-LIVE-023b (anywhere, automated by checks/kpi_keys.py, to write). Data: the key file and PCM's catalog. Steps: run the check; then plant a key PCM reads that the file lacks. Expected: passes on the real files; fails and names the planted key.
- T-LIVE-023c (lab, automated by checks/kpi_keys.py --lab, to write). Expected: each listed key has a sample newer than 10 minutes on at least one lab object, or is marked conditional by PCM-Adapter.

### R-LIVE-024 Cluster Performance matches VCF Operations (M6)

Source: answer to Q-35 ("okay"); [PCM D-131, percentiles labelled by rank](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L139).

Milestone: M6.

Given one lab cluster and the 24-hour window
When its live Performance tab opens
Then the API returns the window's start and end, aligned to 5 minutes
And for that window, Now is the newest 5-minute sample of `vCommunity|Cluster Performance|Cluster Performance Score`, Worst is the lowest sample with its time, and the 5th percentile is taken by nearest rank over the samples
And each equals the reference computed from the Suite API for the same window, at whole percent

Test scenarios:
- T-LIVE-024a (lab, automated by tools/lab/live_reference.py and build/tests/live.lab.test.mjs::test_cluster_performance_matches, to write). Steps: open the tab; read its window from the API; the reference script reads the raw samples for that window and computes Now, Worst and the 5th percentile. Expected: all three equal at whole percent; Worst's time equal; a screenshot is saved.
- T-LIVE-024b (anywhere, automated by build/tests/test_live.py::test_figures_nearest_rank, to write). Data: a fake series of 288 known samples. Expected: Now, Worst, its time and the 5th percentile equal the values computed by hand in the test.

### R-LIVE-025 The other KPIs match VCF Operations (M7)

Source: answer to Q-35; [PCM D-124, the four pages of release 1.0](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L132). The page list waits for round two, because the author has not answered Q-21.

Milestone: M7.

Given the live Performance and Capacity tabs of a lab cluster, a lab ESXi host and a lab VM
When they open on the 24-hour window
Then Cluster Risk, Cluster Consumption, ESXi Performance, VM Performance and Guest OS Performance, and each of their parts, match the reference of R-LIVE-024
And the percentile figure is the 5th where higher is better and the 95th where higher is worse

Test scenarios:
- T-LIVE-025a (lab, automated by tools/lab/live_reference.py and build/tests/live.lab.test.mjs::test_all_kpis_match, to write). Steps: as T-LIVE-024a, for every KPI and part on the three objects. Expected: all equal at whole percent, or at the part's own decimals where its limits have decimals.

### R-LIVE-026 Lines across clusters agree with vSphere World

Source: answer to Q-23; [PCM D-091, the Performance tab above the cluster](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L98).

Milestone: M7.

Given every lab cluster is under the selected node
When its Performance and Capacity tabs above the cluster open
Then the worst and percentile lines are computed from each cluster's published score at each point
And they equal PCM-Adapter's vSphere World metrics (Worst Cluster Performance, Worst 10 Percent Cluster Performance, Worst Cluster Risk, Worst 10 Percent Cluster Risk, Highest Cluster Utilization, Highest 10 Percent Cluster Utilization) at whole percent

Test scenarios:
- T-LIVE-026a (lab, automated by tools/lab/live_reference.py and build/tests/live.lab.test.mjs::test_world_lines, to write). Steps: open the lab's VCF instance node; read the vSphere World keys for the same window. Expected: equal at whole percent at every point. If the lab has one cluster only, the scenario says so and still compares.

### R-LIVE-027 Capacity Remaining, Time Remaining and VM Remaining are read

Source: answer to Q-20 ("yes": live mode reads what the synthetic demo shows as placeholders); [PCM D-100, the KPI first on the Performance and Capacity tabs](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L107).

Milestone: M7.

Given a lab VM, ESXi host or cluster
When its live Capacity tab opens
Then Capacity Remaining and Time Remaining (and VM Remaining on a host and a cluster) are VCF Operations' own values, from the keys in the key list (R-LIVE-023), with their time and the line "From VCF Operations, {time}"
And a value VCF Operations does not hold shows "No data"; no placeholder is shown

Test scenarios:
- T-LIVE-027a (anywhere, automated by build/tests/test_live.py::test_remaining, to write). Data: the fake with the three values on a cluster and none on a VM. Expected: the cluster shows the fake's values and the line; the VM shows "No data".
- T-LIVE-027b (lab, automated by tools/lab/live_reference.py and build/tests/live.lab.test.mjs::test_remaining, to write). Expected: the page shows the same values as the Suite API.

## Agent E2 in the live demo

### R-LIVE-028 Agent E2 gets the live facts in the usual shapes

Source: answer to Q-36 ("agree"); C3.

Given a question asked in the Agent E2 panel of the live demo
When PCM builds the facts
Then they have the same fields and shapes as in the synthetic demo (the screen, the KPI series, the parts at the KPI's worst point, the parts once an hour, the page's KPI series for the suggested questions), filled only with live values from the same reads as the page
And a fact with no data is sent with its value missing and marked "no data"; it is never dropped silently and never filled with a synthetic value
And the list of facts each answer feature needs is the one in C3's specification

Test scenarios:
- T-LIVE-028a (anywhere, automated by build/tests/test_live.py::test_agent_facts, to write). Data: the fake Suite API, with one part key stale; a stub Agent E2 that records the request. Steps: ask "Why the worst?" on Cluster Performance. Expected: the recorded facts have every field of the synthetic request; values equal the page's; the stale part is present and marked "no data".
- T-LIVE-028b (anywhere, automated by checks/agent_e2_api.py, to extend). Data: a live-shaped request with one fact marked "no data". Expected: the real Agent E2 service in mock mode accepts it, and its answer says the fact is missing.

### R-LIVE-029 What the live facts never carry

Source: answer to Q-39 ("yes no issue at all. It's just a lab"); answer to Q-33.

Given a question asked in the live demo
When PCM sends the facts to Agent E2
Then they carry lab object names and values, which may reach the cloud model
And they never carry the VCF Operations password, token or URL
And they carry no story, case, calendar or action record

Test scenarios:
- T-LIVE-029a (anywhere, automated by build/tests/test_live.py::test_facts_clean, to write). Data: the marker password and token of T-LIVE-007b, and a calendar entry in PCM's database. Steps: ask one question on each live page. Expected: no marker, no Suite API URL and no calendar entry in any recorded request.

### R-LIVE-030 Agent E2 names the part that moved the KPI (M6)

Source: answer to Q-35 (the worst part is the one that lost the most points at the worst point, under the adapter's scoring); [W-012, release 1.0 success](../../DECISIONS.md).

Milestone: M6.

Given one lab cluster and the 24-hour window
When the person asks Agent E2 "Why the worst?" on its Cluster Performance
Then Agent E2's answer names, as the main cause, the part the reference identifies: the part that lost the most points at the KPI's worst point under the catalog's scoring
And when no part lost points, the answer says no part pulled the KPI down

Test scenarios:
- T-LIVE-030a (lab, automated by tools/lab/live_reference.py and build/tests/live.lab.test.mjs::test_agent_worst_part, to write). Data: Agent E2 on the lab VM with the gateway key. Steps: the reference script scores every part at the worst point; the page test asks the question and reads the answer. Expected: the answer names the reference's part, judged by the automatic grader of [W-013, Agent E2 in release 1.0](../../DECISIONS.md) when the wording differs.

## Tests and the synthetic demo

### R-LIVE-031 Lab tests run automatically from the laptop

Source: answer to Q-37 ("You forgot you have live access"); [W-018, the lab build and lab tests from the laptop](../../DECISIONS.md); W-011.

Given the author's laptop on the VPN, the read-only credential file in `$HOME\.secrets\`, and the live demo deployed on the lab VM
When one command runs (proposed `pwsh tools/lab/Test-Live.ps1` in PCM)
Then it runs PCM-Adapter's validate.ps1 first and stops with its result if the pack is not collecting
And it runs every lab scenario of this file, writes a screenshot of each live page checked, and prints pass, fail or not run per scenario
And it changes nothing in VCF Operations, vCenter or the lab VM's data

Test scenarios:
- T-LIVE-031a (lab, automated by tools/lab/Test-Live.ps1, to write). Steps: run it. Expected: a result line per lab scenario; screenshots in one folder; exit code 1 if any scenario failed.
- T-LIVE-031b (anywhere, automated by build/tests/test_live.py::test_runner_reports_not_run, to write). Data: an unreachable address in place of the lab. Expected: every lab scenario reports "not run", and the command exits with failure.

### R-LIVE-032 The synthetic demo is unchanged

Source: answer to Q-20 ("The synthetic remains as they are"); W-003.

Given the live demo is added
When the existing synthetic tests run (executive, noc, l2, capacity, store, docs, and the page tests in [build/README.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/build/README.md))
Then all pass, with no test or expected value changed

Test scenarios:
- T-LIVE-032a (anywhere, automated by the existing build/tests suite). Steps: run every test listed in build/README.md on the branch that adds the live demo. Expected: all pass; `git diff` shows no change under spec/tests/ and build/tests/ other than new live files.

## Changes to PCM's own specification

Each line is a change to make in private-cloud-manager in a later pull request. Nothing here is edited yet.

| File | Change |
|---|---|
| [decisions.md, D-076](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L83) and its [rationale](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L406) | Say that the live demo sends lab facts to the cloud model through the gateway (Q-39), and that facts never carry the VCF Operations credential, token or URL. |
| [decisions.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md) | Add a PCM decision for the live demo that points to W-015 and this file. |
| [decisions.md, D-062](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L69) | The VCF APIs are now checked against the lab VCF Operations; record its version. |
| [decisions.md, D-087](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L94) | Add that the live demo's tree is VCF Operations' inventory from the VCF instance down (Q-25). |
| [decisions.md, D-100 rationale](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L800) and [D-106](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L113) | "Release 1.0: placeholder values" becomes "synthetic demo: placeholder or story values; live demo: read from VCF Operations". |
| [design/pcm-core.md, 3.2](https://github.com/e1-rahabok/private-cloud-manager/blob/main/design/pcm-core.md#L46) | PCM reads every KPI, part and check value from PCM-Adapter and computes only for display (Q-23). |
| [design/pcm-core.md, 3.3](https://github.com/e1-rahabok/private-cloud-manager/blob/main/design/pcm-core.md#L67) | Release 1.0 stores no metrics; the live demo reads through with a 60-second cache (Q-30). |
| [design/pcm-core.md, 3.5](https://github.com/e1-rahabok/private-cloud-manager/blob/main/design/pcm-core.md#L108) | Replace "two collection cycles" with the rule of R-LIVE-015 once confirmed. |
| [design/pcm-core.md, 3.13](https://github.com/e1-rahabok/private-cloud-manager/blob/main/design/pcm-core.md#L207) | The live demo is a separate demo, L2 only (Q-20, Q-22). |
| [design/l2-workspace.md, 3.2](https://github.com/e1-rahabok/private-cloud-manager/blob/main/design/l2-workspace.md#L97) | Fix the Compute path to match D-087, and add the live tree. |
| [spec/catalog/l2.yaml](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/catalog/l2.yaml#L111) (L111, L264, L285) | Placeholders become synthetic-only; "PCM keeps its own history" becomes synthetic-only; add a `key` per part from the key list. |
| [spec/catalog/settings.yaml](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/catalog/settings.yaml) | Add the live settings: the Suite API URL, user, password and CA file variable names, cache 60 s, stale after 10 minutes, check late after 30 minutes, read timeout 10 s. |
| `spec/catalog/vcf-operations-keys.yaml` (new) | The key list generated from the lab (R-LIVE-023). |
| [spec/workspaces/l2/monitor.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/workspaces/l2/monitor.md#L48) | The Details placeholder rule becomes synthetic-only; fix the stale band text and part counts at L45 and L46 (see D-108 and D-113). |
| [spec/workspaces/l2/frame.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/workspaces/l2/frame.md) | Add the live frame: Monitor with Performance and Capacity tabs only, no class filter, the failed-read state. |
| [spec/api/l2.yaml](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/api/l2.yaml#L6) | Add the live API prefix, the window start and end in responses, and the 400 for `now` and `enable`. |
| [spec/api/openapi.yaml](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/api/openapi.yaml#L85) (L85, L101) | `now` is synthetic-only; the stale flag follows R-LIVE-015; the live source ID in `Meta.source`. |
| [spec/objects/objects.yaml](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/objects/objects.yaml#L45) (L45, L47, L87) | A live object's ID is its resource ID; class of service and environment are synthetic-only. |
| [spec/README.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/README.md#L49) | Add the live demo to the status table; move each verified assumption out of "to verify". |
| [build/README.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/build/README.md#L275) | Remove the gap "No VCF Operations connector in 1.0"; add the live tests. |
| [deploy/README.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/deploy/README.md#L3) and [deploy/pcm.env.example](https://github.com/e1-rahabok/private-cloud-manager/blob/main/deploy/pcm.env.example) | The live demo connects read-only to VCF Operations; add its variables to `pcm.env`. |
| [demo/README.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/demo/README.md#L21) | The drop-down has the live entry; add a short live demo script. |
| [tools/lab/Test-Lab.ps1](https://github.com/e1-rahabok/private-cloud-manager/blob/main/tools/lab/Test-Lab.ps1#L2) | Read the DPAPI files of W-011 in place of Windows Credential Manager (Q-40). |

## Questions for round two

The questions on this file, with their decisions, are in the [interview, round 2](../interview-round-2.md): Q-63 to Q-71 (and Q-57). The few still open are in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md).
