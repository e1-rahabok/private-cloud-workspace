# Interview, round 2

The second round of the interview, kept as the record. Each question keeps its evidence and recommendation as asked, followed by its status: decided by Claude at the author's request ("You decide", 2026-11-26), answered by the author in conversation, superseded by a later decision, or still open in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md). To change a decision, write under it or open a new question.

Links in this file point at the files as they were when the question was asked.

## A. Across the repositories

### Q-57 How does a user see that Agent E2 is still working? (blocks M6)

You asked this in Q-I3. The two drafts differ: the Agent E2 draft adds job calls that report the current stage ("reading files", "writing", "checking") and a time stamp that moves at least every 10 seconds ([R-E2-007](requirements/agent-e2-service.md)); the isvara.io draft proposed a timer only.

- **Recommendation:** the job calls with stages. PCM and isvara.io show the stage name and the time so far. If the time stamp stops moving for 60 seconds, the screen says Agent E2 stopped, with a button to ask again.

**Status:** Decided by Claude at the author's request (2026-11-26): as recommended: stages and a moving time stamp; a message if it stops for 60 seconds.

### Q-58 Agent E2's new plan (milestones for stage 1)

You said Agent E2's plan is outdated (Q-6). Proposed milestones, replacing M1 to M6 in [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), named A1 to A6 so they do not clash with this workspace's M1 to M7:

| # | Milestone | Done when |
|---|---|---|
| A1 | Repository cleaned for stage 1 | Older benchmarks removed (Q-59); stage 2 text marked; WD-019 applied |
| A2 | Answer set and grader | The free-text answer set and the automated grader built; first report on Gemma 4 31B |
| A3 | Service for two callers | The Agent E2 API additions built (progress, attachments, sources, usage); its contract check passes |
| A4 | Live demo support | Agent E2 answers correctly on facts recorded from the lab |
| A5 | isvara.io support | isvara.io's calls work; where the public Agent E2 runs is measured and chosen (Q-4) |
| A6 | Stage 1 exit | The answer set passes on the shipped settings; spending projected within US$50 a month |
| Ongoing | Knowledge base | Content work continues; the review gate waits until after go-live (Q-10) |
| Stage 2, parked | Local model, offline bundle, live test with blocked network, every file reviewed | Text kept as the target (WD-002) |

- **Recommendation:** approve. Claude then rewrites plan.md in one pull request.

**Status:** Answered by the author in conversation (2026-11-26): update Agent E2's plan. Claude rewrites plan.md with milestones A1 to A6; the author reviews the pull request.

### Q-59 What "remove the older benchmarks permanently" covers

You asked to remove them (Q-12). The survey listed them in [project/archive](https://github.com/e1-rahabok/agent-e2/tree/main/project/archive): the result folders from before 2026-11-16 (about 26 MB), the 20 retired questions, the old harness code and its design notes, the old plan decisions and review, and the retrieval results of 2026-11-14. Live documents that quote old numbers (MISSION.md, README.md, harness/README.md, harness/AGENT.md, benchmark/design.md, benchmark/models.md) are rewritten at the same time.

- **Keep:** the round of 2026-11-16 ([`benchmark/results/20261116-*`](https://github.com/e1-rahabok/agent-e2/tree/main/benchmark/results)), the only one on the current pipeline and the evidence behind Gemma 4 31B; and the question-set history files that about 130 current question files link to.
- **Before deleting:** move the old free-text judge's scoring rubric into the new grader.
- **"Permanently":** deleted on main; git history keeps them. Rewriting history needs a force push and breaks old links, including round 1's.
- **Recommendation:** all three points as written.

**Status:** Answered by the author in conversation (2026-11-26): remove them permanently. Deleted on main, as listed; the round of 2026-11-16 and the question-set history stay; the judge's rubric moves to the new grader first; no history rewrite.

### Q-60 Is PCM's repository renamed?

You changed the heading in [spec/intent.md](intent.md) to "private-cloud-manager"; the repository is [private-cloud-manager](https://github.com/e1-rahabok/private-cloud-manager), and PCM's D-001 says "Private Cloud Management".

- **Recommendation:** keep the name as it is, unless you want the repository renamed; then it is renamed like PCM-Adapter was.

**Status:** Open: in OPEN-QUESTIONS.md: the product's name.

### Q-61 The answer record, and spam on isvara.io

You asked what Q-11 was for. **Purpose:** when an answer is wrong, the fix depends on why: Agent E2 missed the right file, the file is wrong or missing, or the model ignored it. A trace records what Agent E2 read and computed, with which model and knowledge version. isvara.io already saves the question; the answer, the trace and a thumbs up or down are missing.

**Spam and nonsense prompts**, all handled in isvara.io before Agent E2 (Q-47): (a) a free code filter: empty, too short, no letters, very long or repeated text gets a fixed reply and never reaches Agent E2; (b) limits per visitor and address, for example 10 questions an hour; (c) an invisible bot check before the first question; (d) a daily spending stop at about US$1.60; (e) a cheap topic check by a small model, which costs money; (f) sign-in, which you ruled out; (g) logs kept 30 days, with flagged spam left out of reviews.

- **Recommendation:** (a), (b), (c), (d) and (g) now; (e) only if spam still gets through. Agent E2 returns a trace ID and keeps traces 30 days; PCM and isvara.io store question, answer, trace ID and rating.

**Status:** Decided by Claude at the author's request (2026-11-26): the protections of the isvara.io plan; Agent E2 returns a trace ID and keeps traces 30 days.

### Q-62 The four unbuilt Agent E2 features

You were unsure what Q-12 meant. In plain words:

1. **Threshold bands in answers.** Code looks up a value's colour band in the catalog, instead of the model reading the table. The model has misread bands (it called a Co-stop of 7.7% orange; it is red). Done for figures on PCM screens; missing for values typed in a question or read from a screenshot.
2. **Executable flow steps.** Code walks a troubleshooting flow step by step and takes each branch. Today the model reads the flow and follows it itself. Large work.
3. **The capacity consultation.** Agent E2 interviews the user over several turns for a new cluster's capacity plan, then computes it. The calculator exists; the conversation does not.
4. **Screenshot questions.** Already in stage 1 by your answer to Q-I1.

- **Recommendation:** 1 and 4 in stage 1; 2 and 3 after isvara.io goes live, 3 first, as an isvara.io feature.

**Status:** Decided by Claude at the author's request (2026-11-26): the band lookup and screenshots in stage 1; flow steps and the capacity consultation after 1.0.

## B. PCM live demo

From [spec/requirements/pcm-live.md](requirements/pcm-live.md).

### Q-63 Which live pages and objects are in M7?

Q-21 has no answer. **Recommendation:** the Performance and Capacity tabs of a cluster, an ESXi host and a VM, the same tabs above the cluster (the VCF instance and the levels VCF Operations puts between it and the cluster), and the tree. M6 is one cluster's Performance tab.

**Status:** Decided by Claude at the author's request (2026-11-26): as recommended.

### Q-64 Are the stale rules right?

You said: no waiting, say "No data" (Q-27). A rule still needs a number. [R-LIVE-015](requirements/pcm-live.md) proposes: a value is stale when its newest sample is more than 10 minutes old (one 5-minute collection cycle plus one cycle of margin; the adapter's own limit). [R-LIVE-021](requirements/pcm-live.md) proposes: a Periodic Cluster Check result is missing 30 minutes after its window ends, since results can arrive a few cycles late. **Recommendation:** confirm both.

**Status:** Decided by Claude at the author's request (2026-11-26): 10 minutes for a value, 30 minutes for a check result. The author asked for no long wait (Q-27); 10 minutes is one collection cycle plus one of margin.

### Q-65 Where does the live demo live?

**Recommendation:** the same PCM server, page `/live/l2` and API `/api/live/l2/...`, so one deployment serves both demos and no request can mix them.

**Status:** Decided by Claude at the author's request (2026-11-26): as recommended: `/live/l2` on the same server.

### Q-66 Which object types does the live tree show between the VCF instance and the cluster?

"Use the inventory from VCF Operations" (Q-25) may include datacenters and folders, which [PCM D-087](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md#L94) leaves out. **Recommendation:** VCF Operations' VCF chain (VCF instance, workload domain, vCenter, cluster, host, VM), without datacenters and folders; the exact types are read from the lab and recorded.

**Status:** Decided by Claude at the author's request (2026-11-26): the VCF chain, without datacenters and folders.

### Q-67 Does the live tree have a Guest OS node, and the Storage, Network and Management views?

**Recommendation:** no. Compute only; the VM's Performance tab already shows its Guest OS layer.

**Status:** Decided by Claude at the author's request (2026-11-26): compute only.

### Q-68 Until PCM-Adapter makes absent data explicit, is a missing part left out or shown as "No data"?

**Recommendation:** left out ([R-LIVE-020](requirements/pcm-live.md)), so a cluster without memory tiering shows 10 Cluster Risk parts, as the synthetic demo does.

**Status:** Decided by Claude at the author's request (2026-11-26): left out until the adapter makes absent data explicit.

### Q-69 What response time must a live page meet?

Q-8 was answered "already answered", but that answer was about Agent E2, not pages. **Recommendation:** a page in under 5 seconds; each Suite API read stops after 10 seconds.

**Status:** Decided by Claude at the author's request (2026-11-26): a page in under 5 seconds; a Suite API read stops after 10 seconds.

### Q-70 What if the lab is too quiet for the Agent E2 test?

If no part lost points in the last 24 hours, [R-LIVE-030](requirements/pcm-live.md) can only check that Agent E2 says so. **Recommendation:** accept that; add a load generator to the lab build later if you want a real dip in the demo.

**Status:** Decided by Claude at the author's request (2026-11-26): accepted; a load generator may come later.

### Q-71 Which VCF Operations version is the lab?

**Recommendation:** the lab test reads it at sign-in, as PCM-Adapter's validate.ps1 does, and records it in [SYSTEM.md](../SYSTEM.md).

**Status:** Decided by Claude at the author's request (2026-11-26): read at sign-in and recorded in SYSTEM.md.

## C. PCM-Adapter

From [spec/requirements/pcm-adapter.md](requirements/pcm-adapter.md). Q-72 to Q-77 name the new identity, since you said to change everything (Q-2).

### Q-72 Adapter kind

**Recommendation:** `PCM`. Short, matches the product, and VCF Operations shows it as the solution's kind.

**Status:** Decided by Claude at the author's request (2026-11-26): `PCM`.

**Replaced:** by WD-032 (2026-11-27): the pack keeps its vCommunity identity.

### Q-73 Metric key prefix

**Recommendation:** `PCM|`, the same word as the adapter kind, so a key shows which pack published it.

**Status:** Decided by Claude at the author's request (2026-11-26): `PCM|`.

**Replaced:** by WD-032 (2026-11-27): the pack keeps its vCommunity identity.

### Q-74 Display name and description

**Recommendation:** "PCM Adapter" for the display name and the adapter name. Rewrite the description in [resources.properties](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/resources/resources.properties#L7) to say the pack computes the KPIs for PCM.

**Status:** Decided by Claude at the author's request (2026-11-26): "PCM Adapter", with the description rewritten.

**Replaced:** by WD-032 (2026-11-27): the pack keeps its vCommunity identity.

### Q-75 Manifest name

**Recommendation:** `iSDK_PCM`, following the SDK's pattern; verify that the build tool accepts it.

**Status:** Decided by Claude at the author's request (2026-11-26): `iSDK_PCM`, if the build tool accepts it.

**Replaced:** by WD-032 (2026-11-27): the pack keeps its vCommunity identity.

### Q-76 Image path and the old image

**Recommendation:** `ghcr.io/e1-rahabok/pcm-adapter`. Delete the old `vcf-operations-vcommunity` package after the old pack is removed from the lab, because a pak works only while its image exists ([build.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/build/build.md#L14)).

**Status:** Decided by Claude at the author's request (2026-11-26): `ghcr.io/e1-rahabok/pcm-adapter`; the old package is deleted after the old pack leaves the lab.

**Replaced:** by WD-032 (2026-11-27): the pack keeps its vCommunity identity.

### Q-77 Pak file name

**Recommendation:** whatever the build tool makes from the new adapter kind, expected `PCM_<version>.pak`; the release step in [validate.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.md#L135) changes with it.

**Status:** Decided by Claude at the author's request (2026-11-26): the name the build tool makes.

**Replaced:** by WD-032 (2026-11-27): the pack keeps its vCommunity identity.

### Q-78 Names of the shipped dashboards, views and reports

**Recommendation:** remove "vCommunity" from every name, for example "ESXi Host Details". Keep "VOA" in the VCF Optimization Assessment set, where it names the assessment.

**Status:** Decided by Claude at the author's request (2026-11-26): "vCommunity" removed from every name; "VOA" kept.

**Replaced:** by WD-032 (2026-11-27): the pack keeps its vCommunity identity.

### Q-79 Removing the old pack from the lab

It deletes the old keys' history and the old Adapter Instances. **Recommendation:** Claude writes the steps and the importer file; you approve; Claude runs them with the admin credential in one session.

**Status:** Decided by Claude at the author's request (2026-11-26): Claude prepares the steps; the author approves at the time, because it deletes data in the lab.

**Replaced:** by WD-032 (2026-11-27): the pack is upgraded in place, so nothing is removed.

### Q-80 What keeps the old name

**Recommendation:** the dated engineering reviews in [docs/development-guide/engineering-review](https://github.com/e1-rahabok/PCM-Adapter/tree/main/docs/development-guide/engineering-review) stay as written. The README sentence that calls the project a free project "from the vCommunity (VMUG, vExpert, VCP)" stays, because it names the community, not the pack.

**Status:** Decided by Claude at the author's request (2026-11-26): as recommended.

### Q-81 Two rows whose statistic disagrees with your "peak" rule

You said a name with "peak" is a 20-second peak, others a 5-minute average (Q-19). VM Network Dropped Tx reads a 5-minute maximum while its catalog name says "peak"; the memory wait rows read a 20-second peak while their names do not say "peak". **Recommendation:** the catalog's interval is the rule. Add "peak" to the memory wait names. Check on the lab whether a 20-second peak of dropped TX packets exists; if none does, make that row 5-minute and remove "peak" from its name.

**Status:** Decided by Claude at the author's request (2026-11-26): the catalog's interval is the rule; the dropped TX row is checked on the lab.

### Q-82 How a data state is published

You said absent data is fixed in the adapter (Q-28). The draft gives every part and every KPI a state each cycle: 0 counted, 1 excluded while green, 2 not applicable, 3 not collected, 4 no current data, 5 read failed, 6 no usable capacity. **Recommendation:** a numeric metric per part, because a metric has a time stamp every cycle; a property is stored only when it changes, so its time says nothing about the current cycle.

**Status:** Decided by Claude at the author's request (2026-11-26): a numeric state metric per part.

### Q-83 Where the state codes are defined

They are an interface between the adapter and PCM, not domain knowledge. **Recommendation:** the adapter's [metrics reference](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics/README.md) holds the table; contract C2, the KPI metric keys, links to it and its check compares PCM's copy.

**Status:** Decided by Claude at the author's request (2026-11-26): the adapter's metrics reference holds the codes; C2's check compares PCM's copy.

### Q-84 Credential file names

PCM-Adapter's CONTRIBUTING.md forbids lab addresses in code, but WD-011 names the file `vcf-ops-10.115.1.81.xml`. **Recommendation:** `$HOME\.secrets\vcf-ops-readonly.xml` and `vcf-ops-admin.xml`; WD-011 changes to match.

**Status:** Decided by Claude at the author's request (2026-11-26): `vcf-ops-readonly.xml` and `vcf-ops-admin.xml`; WD-011 updated.

### Q-85 The two packet counters in the lab policy

Without them the bad-packets part of Cluster Performance has no data; you did not cover this in Q-38. **Recommendation:** the adapter first reports state 3, not collected; then Claude turns the counters on in the lab policy once you approve.

**Status:** Decided by Claude at the author's request (2026-11-26): state 3 first; the counters are turned on once the author approves, because it changes the lab.

### Q-86 Periodic Cluster Check settings

You asked whether Claude knows how PCM gets them (Q-31). Today they are advanced settings on each adapter instance, readable through `GET /suite-api/api/adapters`, but linking an instance to its clusters takes three more reads. **Recommendation:** the adapter publishes the period, time and percent it used as properties on each cluster, with a window-end metric on each result ([R-ADP-020](requirements/pcm-adapter.md)); the settings keep their defaults from the catalog.

**Status:** Decided by Claude at the author's request (2026-11-26): the adapter publishes the settings it used on each cluster.

### Q-87 Is the scoring formula part of contract C1?

You answered Q-14 "if we're changing formula, yes". **Recommendation:** read as: the formula belongs to the KPI definitions contract, owned by Agent E2 and checked by worked examples, whether or not it changes now. Confirm.

**Status:** Decided by Claude at the author's request (2026-11-26): the formula belongs to C1, checked by worked examples.

**Replaced:** by WD-036 (2026-11-27): the catalog holds data rows only; the formula is explained in Agent E2's knowledge and implemented and tested in the adapter.

### Q-88 Guest OS run queue: per vCPU, or total?

Still open from Q-1. The adapter's part is "Guest CPU Run Queue per vCPU"; the catalog's is "Peak vCPU run queue length". **Recommendation:** if the limits were set per vCPU, rename the catalog row "Peak run queue length per vCPU"; otherwise the adapter changes to the total.

**Status:** Open: in OPEN-QUESTIONS.md: needs the author's field knowledge.

### Q-89 A key column in the catalog

**Recommendation:** each catalog row gets the adapter's key next to its name, so PCM maps keys to names and the C1 check matches on the key ([R-KPI-001](requirements/kpi-definitions.md)).

**Status:** Decided by Claude at the author's request (2026-11-26): a key column in every catalog row.

## D. Agent E2

From [spec/requirements/agent-e2-service.md](requirements/agent-e2-service.md).

### Q-90 The pass bar of the answer set

R-E2-006 sets: mean credit at least 0.75 of 3, at most 5% confidently wrong, no misconception stated as true, and at least 0.67 on each live-demo question. The earlier free-text benchmark scored at most 0.41 for every model ([analysis](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-results-before-2026-11-14/analysis-2026-11-13.md)), but the agent has been rebuilt since. **Recommendation:** keep these as the target, run once, and set the gate from that first run if it is far below.

**Status:** Decided by Claude at the author's request (2026-11-26): the target as written; the gate is set from the first run if that run is far below.

### Q-91 The grader model

You remembered the old free-text answers being graded by Opus 5.5. The run records show a GPT model as judge, because Opus was a model under test and a judge may not be a candidate. In stage 1 Opus is not a candidate. **Recommendation:** Opus 5.5, as you said.

**Status:** Answered by the author in conversation (2026-11-26): Opus 5.5 grades.

### Q-92 Who writes the answer set

**Recommendation:** Claude drafts the 40 questions from the knowledge base and your demo questions; an independent agent tries to break each answer key; you review only the keys it marks uncertain, and grade 20 answers once to check the grader agrees with you.

**Status:** Decided by Claude at the author's request (2026-11-26): Claude drafts; an independent agent tries to break each key; the author reviews only uncertain keys and grades 20 answers once.

### Q-93 The time limit per answer

**Recommendation:** 10 minutes. The longest answer measured so far is about a minute.

**Status:** Decided by Claude at the author's request (2026-11-26): 10 minutes.

### Q-94 Where answer jobs are kept

The progress calls (Q-57) keep each job in the service's memory. That works on one long-running process (the lab VM, or a container host), not as a Vercel Python function. **Recommendation:** include this in the Q-4 measurement; prefer a container host for the public service.

**Status:** Decided by Claude at the author's request (2026-11-26): part of the Q-4 measurement; a container host preferred.

### Q-95 Attachment limits

**Recommendation:** up to 5 images of 5 MB each, and up to 3 CSV files of 200 KB in all; raise them only when a real question needs more.

**Status:** Decided by Claude at the author's request (2026-11-26): 5 images of 5 MB; CSV files up to 2 MB, as for contributions (WD-024).

### Q-96 CSV values read by the model, or computed by code

**Recommendation:** the model reads them as text in stage 1; code computes peaks and percentiles only if the CSV questions of the answer set lose credit on figures.

**Status:** Decided by Claude at the author's request (2026-11-26): read as text in stage 1.

### Q-97 What isvara.io sends besides the question

Still open from Q-46, since "C3" was unexplained there. C3 is contract 3, the Agent E2 API. **Recommendation:** add an optional `page` field (the knowledge file the reader has open, read first) and a `reader` role.

**Status:** Decided by Claude at the author's request (2026-11-26): an optional `page` field and a `reader` role.

### Q-98 A shared secret between isvara.io and Agent E2

**Recommendation:** yes. The public Agent E2 answers only calls carrying a secret known to isvara.io, so nobody can bypass isvara.io's injection guard and limits.

**Status:** Decided by Claude at the author's request (2026-11-26): yes.

### Q-99 When the answer set is rerun

**Recommendation:** on a change of model, prompt or service settings, and before a milestone closes; not on every knowledge edit. One run is about 120 answers and 120 gradings; each run reports its cost.

**Status:** Decided by Claude at the author's request (2026-11-26): as recommended.

## E. isvara.io

From [spec/design/isvara-revamp.md](design/isvara-revamp.md). The 47 features there have their own reply lines.

### Q-100 Do old `/read/...` addresses redirect?

You said the old site goes (Q-44). Old links from search engines and from PCM's decisions would then break. **Recommendation:** redirect each to the topic that covers it, mapped from the book heading each knowledge file records; anything unmatched goes to `/guide`.

**Status:** Decided by Claude at the author's request (2026-11-26): redirect to the article that covers the same section.

### Q-101 Where the source view is served

agent-e2 is a public repository today, but a reader should not depend on that. **Recommendation:** isvara.io serves the source view itself at `/topic/<name>/source`, from the export, with the note that it is written for a model (Q-45).

**Status:** Decided by Claude at the author's request (2026-11-26): served by isvara.io at `/articles/<name>/source`.

### Q-102 Where the role slice comes from

No knowledge file carries a role tag. **Recommendation:** a short list in agent-e2: for each of PCM's four roles, the files that role reads first; isvara.io shows it as a reading path.

**Status:** Superseded: by the three learning paths (WD-027); no role slice.

### Q-103 Do pages say the knowledge is still under review?

Every file is used, drafts included (WD-013). **Recommendation:** one footer line on each topic page: "Written by AI from Agent E2's knowledge base, which is still being reviewed."

**Status:** Decided by Claude at the author's request (2026-11-26): the footer line as recommended.

### Q-104 Is the US$50 a month for the gateway alone?

**Recommendation:** the gateway alone; the daily stop is then about US$1.65.

**Status:** Decided by Claude at the author's request (2026-11-26): the gateway alone.

### Q-105 Limits per visitor

**Recommendation:** 10 questions an hour and 30 a day per address; attachments up to 5 MB each, CSV and PNG or JPEG only.

**Status:** Decided by Claude at the author's request (2026-11-26): as recommended.

### Q-106 Which model rewrites the pages

**Recommendation:** try Gemma 4 31B and one stronger model on the pilot page, compare cost and failed page checks, then choose.

**Status:** Decided by Claude at the author's request (2026-11-26): as recommended.

### Q-107 Do the Fleet Console's own 56 rules go?

**Recommendation:** yes. They are knowledge of isvara.io's own (Q-18).

**Status:** Decided by Claude at the author's request (2026-11-26): yes; the Fleet Console is hidden until its checks come from the catalog.

### Q-108 Does the weekly refresh keep converting the Word books into pages?

You said downloads and the weekly refresh continue (Q-55). **Recommendation:** keep refreshing the downloads; stop converting the books into pages, since nothing will read them.

**Status:** Decided by Claude at the author's request (2026-11-26): downloads keep refreshing; the books are no longer converted into pages.

## F. isvara.io exam

From [spec/requirements/isvara-exam.md](requirements/isvara-exam.md).

### Q-109 One correct option per question?

**Recommendation:** one.

**Status:** Decided by Claude at the author's request (2026-11-26): one.

### Q-110 How many options, and what marks?

**Recommendation:** four options; 3 marks for a correct answer, minus 1 for a wrong one, 0 for none. Random guessing then averages 0; the maximum is 30.

**Status:** Decided by Claude at the author's request (2026-11-26): four options; +3, -1, 0.

### Q-111 One fixed set, or a pool?

**Recommendation (revised 2026-11-26 for the Fun Quiz, feature 33 of the isvara.io plan):** the exam stays one fixed set of 10, dated, so results compare. The Fun Quiz draws its rounds from a larger pool per slice, so a visitor can come back and practise.

**Status:** Decided by Claude at the author's request (2026-11-26): the exam is one fixed set; the quiz draws from a pool.

### Q-112 How the questions stay aligned with Agent E2

They live in isvara.io (Q-56), so they copy facts whose master is Agent E2. **Recommendation:** each question is written from the misconception lines of the files it cites and carries those files' fingerprints; when a cited file changes, the build stops; Claude updates the question in a pull request, a judge rechecks it, and you approve only the changed questions.

**Status:** Decided by Claude at the author's request (2026-11-26): as recommended.

### Q-113 Who approves the first set?

**Recommendation:** you, all 10 once, before go-live.

**Status:** Decided by Claude at the author's request (2026-11-26): the author approves all ten once, before go-live (a task, not a question).

### Q-114 Reasoning after each answer, or at the end?

**Recommendation:** after each answer, with the answer then locked.

**Status:** Decided by Claude at the author's request (2026-11-26): after each answer, then locked.

### Q-115 A score board or a share card?

**Recommendation (revised 2026-11-26):** a board, since your visitor model says "compare scores". Without sign-in, a visitor enters a nickname, as on the 2am game's board today. One board per quiz slice and one for the exam. This changes R-EXAM-007, which today lets nothing but a usage count leave the browser.

**Status:** Superseded: by the isvara.io plan: anonymous percentiles, a share card, boards for one event; no global board (WD-027).

### Q-116 A "not official" line?

**Recommendation:** yes: "Not a Broadcom or VMware certification."

**Status:** Decided by Claude at the author's request (2026-11-26): yes.

### Q-117 Length limits

**Recommendation:** at most 50 words per question and 20 per option, for now.

**Status:** Decided by Claude at the author's request (2026-11-26): as recommended.

### Q-118 Leaving and coming back

**Recommendation (revised 2026-11-26):** progress per slice is kept in the browser, with no time limit, so "track progress" works without sign-in. Only a score the visitor chooses to post goes to the board. Clearing the browser clears the progress; the page says so.

**Status:** Decided by Claude at the author's request (2026-11-26): kept in the browser, no time limit.

## G. Lab build

From [spec/requirements/lab-build.md](requirements/lab-build.md).

### Q-119 Can a nested ESXi host use a virtual NVMe device as its memory tier?

Not proven. **Recommendation:** a first spike builds one nested host and reports whether the tier is accepted, before the rest is built.

**Status:** Decided by Claude at the author's request (2026-11-26): a spike first.

### Q-120 How many nested hosts, and how big?

**Recommendation:** two hosts, so DRS and the cluster parts have something to compare, each small enough to leave the physical lab usable. You name the physical cluster, datastore and network.

**Status:** Open: in OPEN-QUESTIONS.md: the author names the cluster, datastore and network.

### Q-121 A plain vCenter cluster or a VCF workload domain?

**Recommendation:** a plain cluster under the lab vCenter, monitored by the same VCF Operations.

**Status:** Decided by Claude at the author's request (2026-11-26): a plain cluster under the lab vCenter.

### Q-122 ESXi version and licences

**Recommendation:** the same ESXi build as the physical hosts; you confirm the lab licences cover two more hosts.

**Status:** Open: in OPEN-QUESTIONS.md: the author confirms the licences.

## H. isvara.io: the visitor model

Your table of why visitors come (2026-11-26) is now the plan's top level ([spec/design/isvara-revamp.md](design/isvara-revamp.md), section 4, and the site map there). Six features are new: Books (48), Infographics (49), Podcast (50), What's New (51), Manual (52) and Survey (53); Search gains regular expressions (12), and the exam becomes Fun Quiz and the exam (33). These questions settle what the table does not.

### Q-123 Is a Download door right, next to your ten reasons?

Your message says visitors come "to read, ask, download"; the table has no Download row. **Recommendation:** keep Download as an eleventh door, for the books and spreadsheets (features 37, 38).

**Status:** Superseded: the ten doors are gone (WD-027); downloads remain.

### Q-124 Articles: one knowledge file each?

Most knowledge files take 3 to 5 minutes to read; your table says about 10. **Recommendation:** one article per file, as the knowledge base is cut; the reading time is shown, and "Read with" leads to the next file. Joining short files into one article would make articles that no file matches, and section links from Agent E2 would miss.

**Status:** Decided by Claude at the author's request (2026-11-26): one article per knowledge file.

### Q-125 Which books, and who decides their order?

**Recommendation:** start with three: Performance management, Capacity management, and Troubleshooting. Claude drafts each book's order from the knowledge base's folders and links; you approve it once. The order is kept in agent-e2, so isvara.io holds no structure of its own.

**Status:** Superseded: the learning paths give the structure online; the author's books stay as downloads.

### Q-126 The podcast: voice, length and cost

The podcast needs a synthetic voice, which costs money per minute of audio, outside or inside the US$50 a month. **Recommendation:** one voice, a fellow practitioner's tone, one episode per book chapter (10 to 15 minutes); made again only when its articles change; start with one book and measure the cost before doing the rest. You approve the voice from a sample.

**Status:** Superseded: the podcast is dropped (WD-027).

### Q-127 What's New: how much detail, and how are corrections shown?

**Recommendation:** one entry per changed article, with one line on what changed; a correction is marked "Correction" and says what was wrong and what is right now. Small wording changes are grouped into one weekly line, so the list stays readable.

**Status:** Decided by Claude at the author's request (2026-11-26): a weekly summary; corrections marked.

### Q-128 The manual: what does a fork include?

**Recommendation:** the manual covers forking Agent E2 with its knowledge base, PCM and PCM-Adapter, setting them up in one lab, pointing Agent E2 at one's own model, and adding one's own knowledge. isvara.io itself is not in the manual; it stays the author's public site.

**Status:** Decided by Claude at the author's request (2026-11-26): the three product repositories and the parent, copied privately by mirroring (WD-025).

### Q-129 Survey: what is stored, and is anything personal asked?

**Recommendation:** no personal data required. A visitor may leave an email address only to be told about a birds-of-a-feather session they asked for; it is kept apart from the answers and deleted after the session.

**Status:** Superseded: the survey is folded into contributions (WD-024): no personal data.

### Q-130 Birds-of-a-feather sessions: where are they held?

**Recommendation:** you name the events (for example VMware Explore or VMUG meetings) or "online"; the survey lists them, with a free line for another.

**Status:** Open: in OPEN-QUESTIONS.md: the author names the events.

### Q-131 Regular-expression search: who is it for?

It searches in the browser, over every form. **Recommendation:** plain words by default, with a switch for regular expressions, since most visitors will not write them; a short help line gives three examples.

**Status:** Decided by Claude at the author's request (2026-11-26): as recommended.
