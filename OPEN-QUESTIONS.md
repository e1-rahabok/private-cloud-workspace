# Open questions: the interview

The interview before any build (ROADMAP, M1). Four read-only surveys of the repositories, one each, listed every conflict, undecided item, unstated assumption and missing requirement that affects stage 1. This file holds them, merged and grouped. Each has the evidence, a recommendation, and an `Answer:` line.

**How to answer.** Edit this file on GitHub. Under a question, write `Agree` to take the recommendation, or your own answer. To take every recommendation in a section, write `All agreed` under the section heading. Leave a line empty to skip it for now; a question marked "blocks" stops its milestone until answered.

**What happens next.** Claude moves each answer into [DECISIONS.md](DECISIONS.md) or a requirement in [`spec/requirements/`](spec/requirements), with the question ID as its source, and deletes the question here.

## A. Intent

Answers fill [spec/intent.md](spec/intent.md).

### Q-I1 What makes stage 1 a success? (blocks M1)

The goals today are directions (connect PCM to live data, revamp isvara.io). Success needs a few outcomes you could check in a demo or on the site.

- **Recommendation:** three outcomes: (1) a PCM demo where live lab data and ACME data both work and Agent E2 explains a real lab KPI correctly; (2) isvara.io answering with Agent E2 at or below AskIO's cost; (3) every contract checked automatically.

**Answer:**

### Q-I2 Who watches the PCM demo, and what must they believe afterwards? (blocks M3)

This decides which pages must be live, which can stay ACME only, and what "convincing" means.

- **Recommendation:** you name the audience (for example customers' operations leaders, or Broadcom colleagues) and the one sentence they should repeat afterwards.

**Answer:**

### Q-I3 What is Agent E2's stage 1 success, separate from its stage 2 release gate? (blocks M3)

Agent E2's release gate is a multiple-choice benchmark on a local model. Stage 1 users read free-text answers on a cloud model. See Q-5 and Q-6.

- **Recommendation:** stage 1 success is the answer set in Q-5 passing, on the model chosen in Q-7, within the time and cost limits of Q-8 and Q-9.

**Answer:**

### Q-I4 What may PCM-Adapter change in stage 1, and what must it not? (blocks M2)

It runs inside VCF Operations for people other than PCM. Renaming its adapter kind or keys would orphan their instances and content (Q-2).

- **Recommendation:** stage 1 changes only labels, documentation, the fixes in Q-1 and Q-14 to Q-17, and issue #85. No change to the adapter kind, manifest name, keys or image path.

**Answer:**

### Q-I5 Who is isvara.io for, what is success, and what is not done? (blocks M5)

Today it is built from the books for their readers. After the revamp its source is the Agent E2 knowledge base.

- **Recommendation:** for VMware administrators and architects learning to run a private cloud. Success: every approved knowledge file is a page people can read, Agent E2 answers with sources, and the exam exists. Not done: live connections, sign-in, paid content.

**Answer:**

## B. Quality bars for Agent E2's answers

### Q-5 What does "good enough" mean for a free-text answer? (blocks M3)

The release gate scores multiple-choice letters only ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md#L270)). PCM and isvara.io users read free text, which no check verifies ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md#L142): "open answers are not verified"). Open answers were confidently wrong 31 to 41% of the time in an earlier generation ([harness/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/README.md#L86)).

- **Recommendation:** a stage 1 answer set of about 40 free-text questions, split between PCM screens and isvara.io readers. You grade each answer right, partly right, wrong or unsure. The bar: no confidently wrong answer you would act on. Rerun on every change of model or prompt.

**Answer:**

### Q-6 What is "done" for Agent E2 in stage 1? (blocks M3)

Agent E2's own plan defines release 1.0 by stage 2 items: a local model, an offline bundle, a test with blocked egress ([project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md#L20)). Its milestones M1 to M6 also clash in name with this roadmap's.

- **Recommendation:** add a "Stage 1" exit to agent-e2's plan: model chosen (Q-7), Q-5 passed, C3 passing for PCM and isvara.io, time and cost measured. Mark the local items as stage 2. Rename agent-e2's milestones A1 to A6.

**Answer:**

### Q-7 Which model and reasoning setting serve PCM and isvara.io? (blocks M3)

Agent E2's service runs a placeholder, `google/gemma-4-31b-it`, until its model round picks one ([service_config.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/harness/service_config.yaml#L5)). isvara.io runs Gemini Flash and Flash-Lite ([lib/model.ts](https://github.com/e1-rahabok/isvara/blob/main/lib/model.ts#L29)).

- **Recommendation:** one configuration for both apps: the open-weight model agent-e2's round picks (so stage 2 stays possible), reasoning off unless Q-5 shows a gain. Keep the placeholder until the round runs.

**Answer:**

### Q-8 How long may an answer take, and must it stream?

PCM answers take a median of 22 to 29 seconds ([project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md#L32)). Agent E2 returns one JSON body; AskIO streams. A public reader sees nothing for half a minute.

- **Recommendation:** 95% of answers under 45 seconds, with a progress state on screen. No streaming in stage 1. A live PCM page (not the answer) loads in under 5 seconds.

**Answer:**

### Q-9 What may one answer cost, and how is spending capped?

One gateway key and one team budget serve the benchmark, PCM and isvara.io; a benchmark round once stopped on the US$100 budget ([project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md#L183)). W-004 says Agent E2 is cheaper than AskIO, but nothing measures it.

- **Recommendation:** three keys (benchmark, PCM lab, isvara.io), each with a budget and an alert at 80%. AskIO's cost per answer, measured from its question log, is the baseline Agent E2 must not exceed. A per-IP rate limit on isvara.io.

**Answer:**

### Q-10 May unreviewed knowledge files reach answers and public pages?

287 of 288 knowledge files are drafts. Agent E2's mission says release content is reviewed ([MISSION.md](https://github.com/e1-rahabok/agent-e2/blob/main/MISSION.md#L126)), and drafts are served today ([KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md#L49)).

- **Recommendation:** answers may use drafts in stage 1, as today, with a "beta" note on isvara.io. Public pages publish only files you approve on a list; each pilot page's files are reviewed first.

**Answer:**

### Q-11 Who keeps the record of each answer: trace, prompt version, rating?

The mission requires a stored trace and a rating per answer ([MISSION.md](https://github.com/e1-rahabok/agent-e2/blob/main/MISSION.md#L119)); the service stores nothing ([ARCHITECTURE.md](https://github.com/e1-rahabok/agent-e2/blob/main/ARCHITECTURE.md#L374)).

- **Recommendation:** C3 returns a trace ID and prompt version; Agent E2 writes traces to a local file kept 30 days; each app stores question, answer, trace ID and rating.

**Answer:**

### Q-12 Which unbuilt Agent E2 features are in stage 1?

Planned for 1.0 but not built: threshold bands in answers, executable flow steps, the capacity consultation, screenshot questions ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md#L123)). Known wrong band statements appear in demo answers today ([project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md#L44)).

- **Recommendation:** stage 1 gets the threshold-band lookup only. The rest come after M6, unless you want the capacity consultation on isvara.io.

**Answer:**

### Q-13 Where does a session write a question that binds several repositories?

agent-e2 says questions go only to its own file ([CLAUDE.md](https://github.com/e1-rahabok/agent-e2/blob/main/CLAUDE.md#L41)); this workspace says here.

- **Recommendation:** questions about one repository stay in that repository; questions that bind several come here. Amend agent-e2's CLAUDE.md to say so.

**Answer:**

## C. KPI definitions (contract C1)

### Q-1 VM and Guest OS sub-metric names (blocks M2)

PCM-Adapter publishes 11 VM Performance and Guest OS Performance sub-metrics under names other than the Agent E2 catalog's; their limits agree. New finding: a metric key is the adapter's row name and never changes; a label changes only the display name in VCF Operations ([definition.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/definition.py#L46)). The Suite API returns keys, not labels, so PCM must map keys to catalog names itself.

| KPI | Adapter key | Agent E2 catalog |
|---|---|---|
| VM Performance | CPU Co-Stop | Peak CPU Co-stop among any vCPU |
| VM Performance | CPU Ready | Peak CPU Ready among any vCPU |
| VM Performance | CPU Overlap | Peak CPU Overlap |
| VM Performance | Disk Latency | Peak read/write latency among vDisks |
| VM Performance | Network Dropped Tx | Peak network TX dropped packets |
| VM Performance | CPU Run | CPU Net Run |
| VM Performance | Memory Ballooned | VM Memory Ballooned |
| Guest OS Performance | Guest CPU Run Queue per vCPU | Peak vCPU run queue length |
| Guest OS Performance | Guest Disk Queue | Peak disk queue length |
| Guest OS Performance | Guest Free Memory | Free memory |
| Guest OS Performance | Guest Page-Out Rate | Memory page-out rate |

- **Recommendation:** the catalog gets a `key` column (it already has an optional one) holding each adapter key; C1 matches on it; the adapter adds catalog names as labels. Keys stay.
- **Needs your field knowledge:** is "Guest CPU Run Queue per vCPU" the same measure as "Peak vCPU run queue length"?

**Answer:**

### Q-14 Is the scoring formula part of the contract?

The catalog says it uses the adapter's model ([thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml#L25)). The weighting, rounding and missing-data rules exist only as prose in Agent E2 and as code in the adapter; C1 checks limits only. The grey band has no value (Q258 in [author-questions.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/author-questions.md#L48)).

- **Recommendation:** add worked examples to the catalog (inputs, expected score) and have C1 run them through the adapter's scoring code. Grey is not in stage 1.

**Answer:**

### Q-15 Where do the Cluster Performance score bands and the closure levels live?

Cluster Risk and Cluster Consumption have score rows in the catalog; Cluster Performance has none, so its colours exist only in the adapter docs and PCM's spec ([periodic-cluster-check.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics/periodic-cluster-check.md#L74)). The closure levels (20, 40, 60, 80) are not checked.

- **Recommendation:** add a score row for Cluster Performance to the catalog, and extend C1 to the score rows and closure levels.

**Answer:**

### Q-16 Close for Business: one Risk level for every cluster, or one for production and another for non-production?

The adapter closes at orange for every cluster ([periodic-cluster-check.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics/periodic-cluster-check.md#L97)); the catalog has 60 for production and 80 for non-production ([thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml#L100)). Agent E2 would explain a rule PCM does not apply.

- **Recommendation:** keep the adapter's single level for stage 1 (it cannot tell production from non-production) and record that in the catalog.

**Answer:**

### Q-17 Is the buffer part of usable capacity?

Open issue [#14](https://github.com/e1-rahabok/PCM-Adapter/issues/14) says no; the code and the catalog say Usable = Total − HA − Buffer.

- **Recommendation:** keep Total − HA − Buffer and close #14.

**Answer:**

### Q-18 Does isvara.io become a consumer of C1?

isvara.io's tools hold their own copies, for example Bronze overcommit CPU 4 and memory 2 ([analyse.ts](https://github.com/e1-rahabok/isvara/blob/main/lib/rvtools/analyse.ts#L31)), against the catalog's 3 and 1.4 ([thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml#L360)).

- **Recommendation:** yes. isvara.io generates its numbers from the catalog, checked by C1; a tool with no catalog source waits.

**Answer:**

### Q-19 Is each part a 5-minute peak of 20-second values, or a 5-minute average?

PCM colours parts with 20-second levels ([D-108](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md#L115)); what the adapter publishes per part is still "to verify" in PCM's spec ([spec/README.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/spec/README.md#L60)).

- **Recommendation:** record the statistic per key in PCM's key list (Q-29) and colour by the matching catalog interval; leave a part uncoloured when no level matches.

**Answer:**

## D. PCM live mode

### Q-20 Does release 1.0 now include live reads? (blocks M3)

PCM's spec says release 1.0 has no VCF Operations connector and shows placeholder values ([build/README.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/build/README.md#L275), [D-106](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md#L113)).

- **Recommendation:** yes. Every "placeholder" rule becomes "synthetic mode: placeholder or story values; live mode: read from VCF Operations, with time and source".

**Answer:**

### Q-21 Which pages are live in stage 1? (blocks M3)

"Release 1.0 pages" can be read as the four L2 pages of [D-124](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md#L132) or the four workspaces of [D-053](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md#L60).

- **Recommendation:** the four L2 pages (cluster Performance and Capacity, ESXi host Performance, VM Performance) and the L2 inventory tree. M3 is one cluster's Performance tab; M4 is the rest.

**Answer:**

### Q-22 What do the other pages show in live mode? (blocks M3)

Executive, the NOC, Capacity, Docs, and L2 Troubleshoot and Improve need data the lab does not have: cost, recovery, availability minutes, alerts.

- **Recommendation:** a clear state, "Not available in Live VCF Operations; switch to Synthetic ACME". Never synthetic numbers under a live label.

**Answer:**

### Q-23 Does PCM only read the KPIs, never recompute them? (blocks M3)

PCM's core design says PCM computes the models from raw metrics ([pcm-core.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/design/pcm-core.md#L48)); D-096 and W-001 say the adapter computes them. The adapter publishes raw values and scores, not per-part scores or "excluded" flags.

- **Recommendation:** PCM reads every KPI, part and check value. It computes only statistics across objects or time (worst, percentile), and each part's colour from the catalog limits with the adapter's rounding. Fix pcm-core sections 3.2, 3.3 and 3.13.

**Answer:**

### Q-24 Where do region, location, class of service, environment and time zone come from in live mode? (blocks M3)

ACME derives class from a letter in the cluster name ([estate.yaml](https://github.com/e1-rahabok/private-cloud-management/blob/main/spec/data/estate.yaml#L140)), and class is required ([objects.yaml](https://github.com/e1-rahabok/private-cloud-management/blob/main/spec/objects/objects.yaml#L47)). The lab has its own names and probably no tags.

- **Recommendation:** a small live mapping file: the lab is one region and one location with a set time zone; class and environment come from vSphere tags read through VCF Operations; untagged objects show as "Unclassified". Tag the M3 cluster Gold.

**Answer:**

### Q-25 Which inventory tree does live mode build?

D-087 and PCM's catalog say Location, VCF instance, workload domain, down to the cluster; the L2 design says no VCF instance, down to the host ([l2-workspace.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/design/l2-workspace.md#L97)).

- **Recommendation:** D-087's path, filled from VCF Operations' VCF topology where the lab has it, otherwise vCenter as the workload domain. Fix the design text.

**Answer:**

### Q-26 What is an object's ID in live mode?

Synthetic IDs are names such as SG-S-04. Names can repeat across vCenters and change.

- **Recommendation:** the VCF Operations resource ID, with the name as a separate field. Synthetic IDs stay.

**Answer:**

### Q-27 When is a value stale, and what does PCM show? (blocks M3)

When data is missing, the adapter publishes nothing, and a "latest" read returns the last old value as if current ([metrics/README.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics/README.md#L138)). Collection also stops after each pack upgrade until restarted.

- **Recommendation:** a key on an object is stale when its newest sample is older than 15 minutes (3 cycles); "Now" then shows "No data" and the time of the last sample. A failed read or failed login marks the whole source stale. Gaps break the line. One test per case.

**Answer:**

### Q-28 How are data that are absent by design shown?

Some keys are missing on purpose: tiering keys on clusters without memory tiering, bad packets while two policy counters are off (the default), VM rows when no VM is on, and Consumption forced to 100 with no usable capacity ([metrics-and-properties.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics-and-properties.md#L65)). Values built from partial reads look normal (issue [#60](https://github.com/e1-rahabok/PCM-Adapter/issues/60)).

- **Recommendation:** "Not applicable" for keys absent by design, marked conditional in the key list; "Full: no usable capacity" and "No running host" for the Consumption cases; partial reads accepted for the small lab.

**Answer:**

### Q-29 Where is the list of keys PCM reads? (blocks M3)

PCM's spec names keys only for scores; parts have names but no keys ([l2.yaml](https://github.com/e1-rahabok/private-cloud-management/blob/main/spec/catalog/l2.yaml#L114)). For hosts, VMs and vCenter, the keys the adapter declares differ from the keys it publishes (issue [#85](https://github.com/e1-rahabok/PCM-Adapter/issues/85)).

- **Recommendation:** one file in PCM, `spec/catalog/vcf-operations-keys.yaml`: key, object kind, unit, statistic, catalog name, conditional or not. C2 compares it with the keys the adapter's KPI modules publish. Fix #85 before M4.

**Answer:**

### Q-30 Does live mode store metrics, or read through on each request?

PCM's spec keeps its own history ([l2.yaml](https://github.com/e1-rahabok/private-cloud-management/blob/main/spec/catalog/l2.yaml#L264)); D-080 says metrics are never stored. The lab has days of data, not the 13 months ACME has.

- **Recommendation:** read through, with a 60-second cache and no store. Longer windows ask VCF Operations for the maximum per slot, draw nothing before the first point, and say "Data from {date}".

**Answer:**

### Q-31 How does PCM get the Periodic Cluster Check's values and settings?

The check publishes once per fixed window, set on the adapter instance, not on the cluster ([periodic-cluster-check.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics/periodic-cluster-check.md#L38)).

- **Recommendation:** PCM shows the published values with their window end. It reads the settings from the adapter instance if the read-only account can; otherwise it shows "(default assumed)".

**Answer:**

### Q-32 How is the mode carried, and what happens to `now` and `enable`?

A server-wide switch lets two viewers flip each other's data; `now` and `enable` work only on synthetic data ([l2.yaml API](https://github.com/e1-rahabok/private-cloud-management/blob/main/spec/api/l2.yaml#L6)).

- **Recommendation:** a per-request parameter `data=acme|live` in the URL, set by the demo control. In live mode, `now` and `enable` are refused with a visible note.

**Answer:**

### Q-33 What do actions, stories, cases and the calendar do in live mode?

SOP buttons and approvals act on synthetic objects ([deploy/README.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/deploy/README.md#L3)). A synthetic calendar entry could reach Agent E2's facts about a real cluster.

- **Recommendation:** every write is disabled in live mode ("Read-only lab connection"); no stories; findings, cases and Improve show "Not in Live VCF Operations"; records are kept apart by mode.

**Answer:**

### Q-34 How does PCM sign in to VCF Operations?

PCM's settings have nothing for it; PCM's lab script skips certificate checks ([Test-Lab.ps1](https://github.com/e1-rahabok/private-cloud-management/blob/main/tools/lab/Test-Lab.ps1#L65)).

- **Recommendation:** URL, user and password from `/etc/pcm/pcm.env`; the lab CA pinned, no skip-verify; token cached and renewed on 401; a read-only account. PCM itself keeps no sign-in in stage 1, behind the lab firewall.

**Answer:**

### Q-35 What exactly does "matches VCF Operations" mean in a test? (blocks M3)

VCF Operations shows no percentile for an arbitrary window and no "worst part". PCM labels Cluster Performance's figure the 5th percentile ([D-131](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md#L139)).

- **Recommendation:** the reference is a test script that reads the raw 5-minute points from the Suite API for the last 24 hours. Now is the last point, Worst the minimum, the 5th percentile by nearest rank, equal at whole percent. The worst part is the one that lost the most points at the worst point, under the adapter's scoring.

**Answer:**

### Q-36 Which facts must PCM send Agent E2 in live mode, and what if one is missing?

ACME sends every fact. Live keys may lack hourly parts or the check values, and Agent E2's opening and worst-part line then disappear without notice ([ARCHITECTURE.md](https://github.com/e1-rahabok/agent-e2/blob/main/ARCHITECTURE.md#L54)).

- **Recommendation:** C3's specification lists the facts each answer feature needs; C3's check adds a live-shaped case; Agent E2 says when a needed fact is missing.

**Answer:**

### Q-37 How is live mode tested without the lab?

PCM's tests assume synthetic data with a fixed clock.

- **Recommendation:** recorded, cleaned Suite API responses as fixtures, and a fake Suite API for unit and page tests (missing key, timeout, 401). One separate lab smoke test.

**Answer:**

### Q-38 Lab facts to confirm before M3

- The exact VCF Operations version (the spec assumes 9.1; [D-062](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md#L69)).
- Whether any lab host has memory tiering.
- Whether the two packet counters are active in the lab policy.
- The host power and maintenance values the adapter has not checked live (issue [#2](https://github.com/e1-rahabok/PCM-Adapter/issues/2)).
- **Recommendation:** Claude reads all four from the lab, read-only, and records them in SYSTEM.md; you turn on the packet counters.

**Answer:**

### Q-39 May live lab facts go to the cloud model?

D-076 says the demo sends only synthetic ACME data ([decisions.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md#L406)). Live mode sends lab object names and metrics through the gateway.

- **Recommendation:** yes for your own lab; amend D-076. Facts never carry credentials or IP addresses.

**Answer:**

## E. Credentials and the rename

### Q-40 One standard for lab credentials

DECISIONS W-011 is wrong about today. PCM-Adapter's tools read `.secrets/vcf-ops.xml` inside the repository folder, with the admin login ([validate.ps1](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.ps1#L32)). PCM's lab script reads Windows Credential Manager ([Test-Lab.ps1](https://github.com/e1-rahabok/private-cloud-management/blob/main/tools/lab/Test-Lab.ps1#L2)), which was your first idea.

- **Options:** (a) DPAPI files in `$HOME\.secrets\`; (b) Windows Credential Manager. Only your Windows account can read either. (b) has a Windows screen to manage it; (a) needs no extra module in PowerShell.
- **Recommendation:** (a), with two files: a read-only account for reading and validating, the admin account for install and restart. Change both repositories' scripts to it.

**Answer:**

### Q-2 The `vCommunity|` prefix and the pack's identity

The adapter kind `vCommunity`, the manifest name, the keys and the container image path identify the pack to VCF Operations; changing them orphans every installed instance ([constants/main.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/constants/main.py#L4), [build.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/build/build.md#L14)).

- **Recommendation:** keep all four. Change only display names, titles, badges and repository links. Keep the pak file name.

**Answer:**

### Q-3 Renaming references in the child repositories

The old repository name appears in agent-e2 (10 files), PCM-Adapter (12) and private-cloud-management (3). GitHub redirects the old links.

- **Recommendation:** one pull request per repository in M2, leaving archive files as they are.

**Answer:**

## F. isvara.io

### Q-4 Where the public Agent E2 runs, and who guards it (blocks M6)

Agent E2 binds to the loopback with no sign-in ([answer_service.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py#L563)). isvara.io is open to all and has its own injection checks.

- **Options:** (a) a Vercel Python function; (b) a small container host; (c) logic copied into isvara (breaks W-001).
- **Recommendation:** isvara.io stays the only public entry, keeps its injection checks and rate limit, and calls Agent E2 with a shared secret. Choose (a) or (b) after measuring start-up time and cost in M5.

**Answer:**

### Q-41 What does Agent E2 give isvara.io to build pages from? (blocks M5)

Nothing today: the export tool writes benchmark attachments only ([export_generator](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/export_generator/README.md#L1)). agent-e2's plan says isvara.io is generated by AI in your fork ([plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md#L31)).

- **Recommendation:** agent-e2 publishes an export, one JSON per published file (id, title, sections, misconceptions, catalog values filled in, images, links, status), with its commit. isvara.io builds pages from it at build time. A check proves every link and image resolves.

**Answer:**

### Q-42 A faithful render of each knowledge file, or an AI rewrite into prose? (blocks M5)

Knowledge files are written for a model: one fact per bullet, no narrative ([KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md#L74)).

- **Recommendation:** render the facts as written (bullets, tables, values; misconceptions in a "common misreadings" box). An optional short AI introduction per page, kept per commit and checked: every number in it must be in the source file.

**Answer:**

### Q-43 In what order does a reader meet the pages?

The books had 5 parts and 50 chapters; the knowledge base has 288 topic files and no reading order.

- **Recommendation:** a small ordered list in agent-e2 (sections, each a list of file IDs); its check confirms every published file appears once.

**Answer:**

### Q-44 Do old `/read/...` links redirect, and where does each page's search description come from?

About 130 links inside isvara.io, plus outside links (PCM's decisions, search engines), point at `/read/...` pages ([sitemap.ts](https://github.com/e1-rahabok/isvara/blob/main/app/sitemap.ts#L38)). Knowledge files have no description field.

- **Recommendation:** a permanent redirect from each old page to its new page, using the book heading each knowledge file records. The description comes from the file's first bullet, checked for length.

**Answer:**

### Q-45 How does an answer cite pages?

AskIO writes `/read/...` links into its text, and the eval checks for them ([evals/run.mjs](https://github.com/e1-rahabok/isvara/blob/main/evals/run.mjs#L26)). Agent E2 removes file references from its text and returns them separately ([answer_service.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py#L326)).

- **Recommendation:** isvara.io turns Agent E2's `files_read` into a Sources list of page links, through the export's ID-to-page map.

**Answer:**

### Q-46 What must C3 add for isvara.io?

C3 knows PCM's roles only and has no page context ([answer_service.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py#L63)). isvara.io's chat knows the chapter being read; its MCP tool `ask_isvara` also calls the agent.

- **Recommendation:** an optional `page` field and a `reader` role, added the safe way (expand first); the chat supports Agent E2's clarifying round; `ask_isvara` goes through the same call. No images in stage 1.

**Answer:**

### Q-47 Who owns the public conduct rules, and may public answers look things up on the web?

isvara.io's prompt holds an injection guard, British English, a neutral rule on migration and a docs lookup ([lib/prompt.ts](https://github.com/e1-rahabok/isvara/blob/main/lib/prompt.ts#L21)); they go when AskIO goes. Agent E2 has web lookup off, because PCM sends customer data ([service_config.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/harness/service_config.yaml#L31)).

- **Recommendation:** Agent E2 owns the conduct rules as a public caller profile. Web lookup (vendor documents and URLs users give) is on for isvara.io, off for PCM.

**Answer:**

### Q-48 Do isvara.io's "load-and-ask, no retrieval" rules retire?

isvara.io's CLAUDE.md and PLAN.md forbid retrieval, a database and a vector store ([CLAUDE.md](https://github.com/e1-rahabok/isvara/blob/main/CLAUDE.md#L10)); Agent E2 retrieves.

- **Recommendation:** yes. Rewrite them in isvara.io's first pull request; `/api/chat` becomes a thin call to Agent E2.

**Answer:**

### Q-49 Is the Operations Score rescored on the catalog?

isvara.io's score uses the book's four indicators and a 4× curve ([lib/opsScore.ts](https://github.com/e1-rahabok/isvara/blob/main/lib/opsScore.ts#L34)); the knowledge base has no performance SLA and five limits per metric ([kpi-vs-sla.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md#L4)). The curve feeds the home dial, /tools, /assess, /estate, the MCP tools and the 2am game.

- **Recommendation:** yes. One module generated from the catalog; the 4× curve goes.

**Answer:**

### Q-50 Which of the ten tools stay?

Two are ports of the Excel files ([CLAUDE.md](https://github.com/e1-rahabok/isvara/blob/main/CLAUDE.md#L408)); the catalog has no cost or price rows; the SLA builder conflicts with "no performance SLA".

- **Recommendation:** keep a tool only where Agent E2 holds its knowledge: the capacity planner from Agent E2's calculator; park the cost calculator and the SLA builder; ground the maturity tool on the SP5 files.

**Answer:**

### Q-51 What does /assess become?

It weighs four readings (the old score) and five practice questions ([Assess.tsx](https://github.com/e1-rahabok/isvara/blob/main/app/_signal/screens/Assess.tsx#L10)).

- **Recommendation:** a self-assessment of SP5 practice only, from the knowledge base's health-check and operations files.

**Answer:**

### Q-52 Does the MCP endpoint stay?

It offers `ask_isvara`, `ops_score`, `health_check`, `fleet_view` and the books as resources ([MCP.md](https://github.com/e1-rahabok/isvara/blob/main/MCP.md#L14)).

- **Recommendation:** keep it. `ask_isvara` calls Agent E2, `ops_score` is rescored, and the resources come from the export. `health_check` and `fleet_view` stay: the caller sends the data, and isvara.io connects to nothing.

**Answer:**

### Q-53 Do /estate (RVTools health check) and /fleet stay?

Each of the 13 checks cites a book passage that disappears ([CLAUDE.md](https://github.com/e1-rahabok/isvara/blob/main/CLAUDE.md#L283)).

- **Recommendation:** keep both, with files staying in the browser. Ground each check on a catalog row or knowledge file; a check with no source is marked "to review".

**Answer:**

### Q-54 What does "the evals pass" mean? (blocks M6)

The eval prints a count and never fails ([evals/run.mjs](https://github.com/e1-rahabok/isvara/blob/main/evals/run.mjs#L34)). Three expectations describe AskIO's behaviour, and one expects a refusal that contradicts the restriction you lifted ([queries.json](https://github.com/e1-rahabok/isvara/blob/main/evals/queries.json#L18)).

- **Recommendation:** rewrite the expectations from the knowledge base; the eval fails on any miss. Pass: all 20 answers cite a published page and contain each question's key fact. The injection battery is unchanged, with 0 violations.

**Answer:**

### Q-55 Where is the revamp built, and when is it done? (blocks M5)

- **Recommendation:** on a branch of isvara, deployed as a Vercel preview, switched over in one release. Done when every approved file has a page, old links redirect, the evals pass, lint, type check and build pass, cost and time limits hold, and the 2am game's citations point at new pages. /download stays as an archive marked "the books may differ from the guide"; the weekly Word refresh stops.

**Answer:**

## G. The exam

### Q-56 What is the exam's format, and where are its questions kept? (blocks M7)

- **Recommendation:** one fixed set of 10 multiple-choice questions, written from the knowledge base's misconceptions and never copied from the benchmark; kept in agent-e2 (not indexed); each answer cites its pages; scored in the browser with no model call; the reasoning shown after each answer.

**Answer:**

## Fixes Claude makes without asking

Each is a mistake with only one right answer. Say so here if you object.

- PCM: two decisions numbered D-114 ([decisions.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md#L121)); `l2.log_noise_max` defined twice ([settings.yaml](https://github.com/e1-rahabok/private-cloud-management/blob/main/spec/catalog/settings.yaml#L244)); three different counts of Cluster Risk parts in the text (D-106, D-113, l2.yaml).
- PCM-Adapter: "5 sub-metrics" should be 6 ([metrics-and-properties.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics-and-properties.md#L79)); issues #2 and #94 are out of date.
- agent-e2: SECURITY.md understates model calls per answer ([SECURITY.md](https://github.com/e1-rahabok/agent-e2/blob/main/SECURITY.md#L31)); two documents say the service runs 3 samples, its config says 1 ([service_config.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/harness/service_config.yaml#L32)).
- isvara: CLAUDE.md says three books; there are five.
