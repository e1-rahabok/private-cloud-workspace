# Decisions

Decisions that bind more than one repository. A decision inside one repository goes in that repository's own log:

| Repository | Its decision log |
|---|---|
| agent-e2 | [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) |
| PCM-Adapter | Its issues and pull requests |
| private-cloud-manager | [decisions.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md) |
| isvara | [PLAN.md](https://github.com/e1-rahabok/isvara/blob/main/PLAN.md) |

One entry each, newest at the bottom. A changed decision is edited in place; git keeps the history. Each entry has a heading with its ID, the decision, and the reason. "Q-" IDs are the author's answers in the [interview, round 1](spec/interview-round-1.md); other IDs are explained in the [glossary](spec/glossary.md).

## WD-001 Agent E2 as the source of domain knowledge

- **Date:** 2026-11-25
- **Decision:** Agent E2 is the source of all domain knowledge: KPI names, parts, limits, scoring, thresholds, flows and explanations. The VCF vCommunity Adapter implements the KPIs. PCM and isvara.io consume; isvara.io holds no knowledge of its own (Q-15, Q-18). A change to domain knowledge starts in agent-e2.
- **Reason:** With one master copy, every other copy can be generated from it or checked against it ([C1, KPI definitions](spec/glossary.md#c1)).

## WD-002 Release 1.0: lab demo, cloud model

- **Date:** 2026-11-25
- **Decision:** Release 1.0 is a demo in the lab. PCM runs in the lab, and Agent E2 uses a cloud model through Vercel AI Gateway. A customer's on-premises deployment with a local model comes after release 1.0 and is out of scope.
- **Reason:** A plan that describes two futures at once leads each session to build toward the wrong one. Text about the on-premises deployment stays in the child repositories as the target.

## WD-003 Synthetic and live demos kept apart

- **Date:** 2026-11-25
- **Decision:** PCM keeps its synthetic ACME demo unchanged and adds a separate live demo as a new entry in the demo drop-down. The two are separate demos, never switched inside one page. Details: WD-015.
- **Reason:** The lab has too little activity to show Agent E2; the live demo proves PCM reads real data (Q-20, Q-32).

## WD-004 Two web apps sharing Agent E2

- **Date:** 2026-11-25
- **Decision:** PCM (private) and isvara.io (public) are two web apps. Both use Agent E2 for knowledge, through the same Vercel AI Gateway. isvara.io connects to no live system. Agent E2 replaces AskIO on isvara.io.
- **Reason:** Both apps then give the same answers from the same knowledge. Agent E2's model costs less per call than AskIO's, but it holds conversations and reads CSV files and screenshots, so the cost per visitor may rise (Q-I1); the budget is WD-014.

## WD-005 isvara.io content from the knowledge base

- **Date:** 2026-11-25
- **Decision:** isvara.io's content will come from the Agent E2 knowledge base, not from the Word and Excel files. The guide, the tools and the assessment pages are rebuilt (WD-017).
- **Reason:** isvara.io then holds no copy of the knowledge that could drift from Agent E2 (WD-001).

## WD-006 An exam for people on isvara.io

- **Date:** 2026-11-25
- **Decision:** isvara.io gets an exam for people: 10 short, very hard multiple-choice questions that test depth of understanding, not calculation. A wrong answer loses marks; no answer scores 0. The exam is kept in isvara.io. It is separate from Agent E2's benchmark, which tests the machine.
- **Reason:** A people's exam and a machine benchmark have different purposes (Q-56).

## WD-007 PCM-Adapter's new name and identity

- **Date:** 2026-11-25
- **Decision:** VCF-vCommunity-Adapter is renamed PCM-Adapter: the repository, and also the pack's identity in VCF Operations (WD-016).
- **Reason:** PCM D-096: the adapter is part of PCM. The author confirmed no installed instance needs protecting (Q-2, Q-I4).
- **Status:** the repository is renamed; the pack's identity in VCF Operations stays, by WD-032.

## WD-008 Decision logs per repository

- **Date:** 2026-11-25
- **Decision:** Each repository keeps its own decision log. This file holds only decisions that bind more than one repository, plus the index above.
- **Reason:** A cross-repo session needs one place to look; a single-repo session already has its own.

## WD-009 Git workflow in the early phase

- **Date:** 2026-11-25
- **Decision:** Git workflow: see [CLAUDE.md](CLAUDE.md), section Git. One branch and pull request per change per repository. While the project is early (defining scope and documentation), Claude merges every pull request itself once the checks pass, and warns the author about a major change in the pull request text and in its report. Revisit when the products have users.
- **Reason:** The author, 2026-11-25: early work is mostly scope and documentation, so waiting for review costs more than it saves. The warning keeps the author aware of what spreads to other repositories.

## WD-010 Contract checks in code

- **Date:** 2026-11-25
- **Decision:** Contracts between repositories are checked by code in [`checks/`](checks). A pull request that breaks a check is not merged. Known gaps are a baseline that only shrinks. Every contract has a check (Q-I1).
- **Reason:** Without a check, the two sides of a contract drift apart and nobody notices until something breaks.

## WD-011 Lab credentials

- **Date:** 2026-11-25
- **Decision:** Lab credentials. On the author's laptop: two DPAPI files in `$HOME\.secrets\` (`Export-Clixml`), one for a read-only VCF Operations account (reading and validating) and one for the admin account (installing and restarting the pack); the scripts of the VCF vCommunity Adapter and PCM change to read them. On the PCM lab VM: `/etc/pcm/pcm.env`, root and group `pcm` only.
- **Reason:** Agreed (Q-40). Before this, the VCF vCommunity Adapter's scripts read an admin login from a file inside the repository folder, and PCM's lab script read Windows Credential Manager.

## WD-012 Release 1.0 success

- **Date:** 2026-11-25
- **Decision:** Release 1.0 succeeds when VMware colleagues and customers who see the PCM demo find it useful and want to fork the repositories privately, to customise and deploy in their own private cloud; when Agent E2 explains a real lab KPI correctly in the live demo; and when every contract is checked automatically.
- **Reason:** The author's answers to Q-I1 and Q-I2.

## WD-013 Agent E2 in release 1.0

- **Date:** 2026-11-25
- **Decision:** Agent E2 in release 1.0: accuracy comes before speed; an answer may take minutes; no streaming, but the user always sees that Agent E2 is still working. Free-text answers are graded automatically by a strong model as judge, as Agent E2's earlier free-text benchmark was. The model is Gemma 4 31B, or a later version when one comes. Every knowledge file is used, drafts included; a review gate on files waits until after go-live.
- **Reason:** The author's answers to Q-I3, Q-5, Q-7 and Q-10.

## WD-014 Spending on Vercel AI Gateway

- **Date:** 2026-11-25
- **Decision:** Spending on Vercel AI Gateway is tracked by the author on vercel.com. A benchmark run has a budget of US$100. After isvara.io goes live, it must stay within US$50 a month (the Vercel subscription is already US$40).
- **Reason:** The author's answer to Q-9. The US$50 limit is a roadmap task after go-live.

## WD-015 PCM's live demo

- **Date:** 2026-11-25
- **Decision:** PCM's live demo: the L2 workspace only, for performance and capacity management only. Its inventory comes from VCF Operations and starts at the VCF instance; an object's ID is its VCF Operations resource ID. Class of service, region, environment and time zone exist only in the synthetic demo. PCM shows what the VCF vCommunity Adapter publishes and says "No data" when a value is stale. It reads through with a 60-second cache and stores no metrics. It may compute for display, and never writes to VCF Operations. Lab facts may go to the cloud model. Actions, stories, cases and the calendar are out of 1.0.
- **Reason:** The author's answers to Q-20 to Q-39. Requirements: [spec/requirements/pcm-live.md](spec/requirements/pcm-live.md).

## WD-016 Scope of change for the VCF vCommunity Adapter

- **Date:** 2026-11-25
- **Decision:** The VCF vCommunity Adapter may change anything, including its adapter kind, manifest name, metric key prefix, image path and pak name. A metric's key comes from the adapter; its name comes from Agent E2's catalog. All scoring logic comes from Agent E2, including the score bands and the closure levels. One Cluster Risk level for every cluster. Usable capacity is Total − HA − Buffer. A metric whose name says "peak" is a 20-second peak; others are 5-minute averages. Data absent by design is made explicit by the adapter.
- **Reason:** The author's answers to Q-I4, Q-1, Q-2, Q-14 to Q-17, Q-19 and Q-28. Requirements: [spec/requirements/pcm-adapter.md](spec/requirements/pcm-adapter.md).
- **Status:** the adapter kind, manifest name, key prefix, image path and pak name stay, by WD-032. Data absent by design is made explicit after release 1.0, by WD-033. "Comes from Agent E2" means: stated in Agent E2's knowledge and catalog, implemented in the adapter's code, and compared by the C1 check, by WD-036.

## WD-017 isvara.io rebuild

- **Date:** 2026-11-25
- **Decision:** isvara.io is rebuilt: same look and feel, new functionality; the old site goes. Its pages are AI rewrites of Agent E2's knowledge files, with no AI-speak. A cited source opens the knowledge file, with a note that it is written for a model. The injection guard sits in isvara.io, before it calls Agent E2. The "load-and-ask" design retires. Downloads and the weekly Word refresh continue. It is built on a branch with a Vercel preview and switched over in one release. Each feature waits for the author's review in [spec/design/isvara-revamp.md](spec/design/isvara-revamp.md).
- **Reason:** The author's answers to Q-41 to Q-55.

## WD-018 Lab build for memory tiering

- **Date:** 2026-11-25
- **Decision:** The physical lab hosts have no memory tiering. The new repository [lab-build](https://github.com/e1-rahabok/lab-build) builds nested virtual ESXi hosts with memory tiering automatically, so tiering features can be tested. Tests run against the live lab from the author's laptop, using the PCM-Adapter repository's tools to install, validate and take screenshots.
- **Reason:** The author's answers to Q-37 and Q-38. Requirements: [spec/requirements/lab-build.md](spec/requirements/lab-build.md).
- **Status:** after release 1.0, by WD-031.

## WD-019 Place for questions across repositories

- **Date:** 2026-11-25
- **Decision:** A question about one repository stays in that repository's question file; a question that binds several repositories goes to this workspace's [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).
- **Reason:** The author's answer to Q-13.

## WD-020 No bare short names

- **Date:** 2026-11-25
- **Decision:** No bare short names. A document uses an ID such as C3, WD-012 or Q-27 only with its meaning, or as a link to the [glossary](spec/glossary.md), on first use.
- **Reason:** The author could not tell what "C3" meant (Q-46).

## WD-021 Agent E2's plan and older benchmarks

- **Date:** 2026-11-25
- **Decision:** Agent E2's plan is rewritten for release 1.0, and its older benchmarks are removed permanently.
- **Reason:** The author's answers to Q-6 and Q-12: the outdated material confuses readers and Claude.

## WD-022 isvara.io organised by visitor reasons

- **Date:** 2026-11-26
- **Decision:** isvara.io is organised by why its visitors come: to read (articles, books, infographics), ask (Agent E2), listen (podcast), solve (calculators), catch up (What's New), fork (manual), find (search, with regular expressions), practise (Fun Quiz), engage (survey), and download. Each is a door in the header and on the home page; every feature sits behind one. All forms come from the same knowledge files.
- **Reason:** The author's visitor model, 2026-11-26. Recorded for history; the plan now follows WD-027.
- **Status:** replaced by WD-027. The visitor model was a suggestion; the three learning paths became the backbone. Its ideas that remain (infographics, What's New, the manual, search, practice) are in the isvara.io plan.

## WD-023 Writing rules for people and for machines

- **Date:** 2026-11-26
- **Decision:** Documents for people follow Agent E2's writing rules ([writing.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/writing.md)) and its list of flagged phrases (`avoid_ai_speak` in [rules_check_values.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/rules_check_values.yaml)): plain sentences, no flagged phrases, no slogans or "X, not Y", headings as noun phrases of at most 9 words, short table cells. Documents for machines (the CLAUDE.md files, requirements, templates) are written for an agent to follow: one rule per bullet, exact paths and names, the trigger before the action. The general rules and the list of flagged phrases move from agent-e2 to this workspace in M2, since they apply to every repository; agent-e2 keeps the rules particular to knowledge files. [tools/style.py](tools/style.py) checks every repository on its pull requests (R-WS-006). The same rules apply to commit messages and pull request text.
- **Reason:** The author has fixed AI-speak in Agent E2 several times (2026-11-26). One copy of the rules, checked by code, keeps every repository consistent.

## WD-024 Contributions from release 1.0

- **Date:** 2026-11-26
- **Decision:** isvara.io accepts contributions from release 1.0: a correction, an addition or something to review, with a note, one link and up to three files (PNG, JPEG, CSV). They go to a private queue and are never published automatically; the author decides each week from an AI-sorted list, and accepted items become source notes in agent-e2. Contributors may stay anonymous; credit is shown only with a public profile link, checked at review. No email address is collected. Contributors agree, in one sentence, that they may share it, that it holds no confidential customer data, and that it may be used, changed and published. Files are deleted once processed, and after at most 30 days; no IP address is kept with a contribution. Limits: 3 contributions a day per address, 3 files, 5 MB per image, 2 MB per CSV file, 2,000 characters, 1 link, 100 contributions a day in total; all are settings. There is no masking in 1.0: visitors remove IP addresses and host names before uploading. Protection against floods, bots, large or disguised files and indecent images is described in the [isvara.io plan](spec/design/isvara-revamp.md), section Protection.
- **Reason:** The author wants the vCommunity to give feedback, corrections and files from 1.0, and asked Claude to decide the details as the one who knows public websites (2026-11-26). Nothing published without review removes the incentive for spam; no account and no email address keep the barrier low and the personal data nil.

## WD-025 The product and how customers take it

- **Date:** 2026-11-26
- **Decision:** The product is Agent E2, the VCF vCommunity Adapter and PCM, which customers take together, with this parent workspace. The VCF vCommunity Adapter alone is the simplest deployment (one pak file, no Linux), without Agent E2; its documentation presents it as one part of the whole and points to the knowledge rather than repeating it. PCM runs as a Linux container, with VKS integration. isvara.io is a separate public site that customers use but never install or copy. Customers copy the product privately by mirroring each repository into a private one, since a fork of a public repository on GitHub is always public; the manual says so.
- **Reason:** The author, 2026-11-26.

## WD-026 Release 1.0 scope

- **Date:** 2026-11-26
- **Decision:** The knowledge covers Day 2: running, monitoring, troubleshooting and planning. Design, installation, building, configuration and upgrades are out, and Agent E2 says so when asked. After 1.0: personal dashboards in PCM, what-if analysis, the people side of operations, and depth beyond vSphere (breadth grows through contributions). The product track comes before a separate knowledge track. The audience of Agent E2 and PCM is the VMware administrator first; the CIO is not a focus for Agent E2.
- **Reason:** The author, 2026-11-26: Day 1 knowledge depends on the release; release 1.0 must be small enough to finish.

## WD-027 isvara.io plan and the knowledge model

- **Date:** 2026-11-26
- **Decision:** isvara.io follows the [isvara.io plan](spec/design/isvara-revamp.md): the three learning paths as navigation; articles rewritten from knowledge files; infographics as a core feature; Ask Agent E2; contributions; a quiz with a mastery map, the exam and the 2am game; calculators on the catalog; a weekly summary of changes. Dropped: the podcast, the Operations Score, the cost calculator and SLA builder, the self-assessment, a global leaderboard. The [knowledge model](spec/knowledge-model.md) (three paths, four lenses as a completeness check, depth, experience, scale notes) is shared by Agent E2, isvara.io and the knowledge factory.
- **Reason:** The author's paths and answers of 2026-11-26, and Claude's decisions at the author's request on the details. Replaces WD-022.

## WD-028 The product's name

- **Date:** 2026-11-26
- **Decision:** The product is Private Cloud Manager, PCM for short. The books keep "Private Cloud Management" as the name of the discipline. PCM's own D-001 ("Private Cloud Management") is updated in PCM's decision log in M2. The repository was renamed from private-cloud-management to [private-cloud-manager](https://github.com/e1-rahabok/private-cloud-manager) on 2026-11-26; GitHub redirects the old address.
- **Reason:** The author, 2026-11-26: "Manager, not Management" (round 3, Q-60).

## WD-029 No licence file for now

- **Date:** 2026-11-26
- **Decision:** The repositories keep no licence file for now, as today.
- **Reason:** The author, 2026-11-26 (round 3, Q-133).
- **Consequence:** without a licence, ordinary copyright applies: GitHub's terms let others view a public repository and fork it on GitHub, but give no permission to copy it elsewhere, change it or run it. That conflicts with principle 4 (forkable: customers copy the product privately and customise it) and with the contributions agreement of WD-024. Revisit before the first customer copies the product; this is not legal advice.


## WD-030 Guessable names

- **Date:** 2026-11-27
- **Decision:** In every repository, an ID, term, heading, folder or file name can be guessed from itself. Each concept has one word; a name uses two words when one would be ambiguous, as Agent E2's knowledge folders do. Folder and file names carry no version, milestone or status word (such as v5, m5, proto, new, old or final), because git keeps the history. When a name stops being true, it is renamed in every file, and no text explains the exception.
- **Reason:** The author, 2026-11-27: "The best documentation is No Documentation." Every session, person or AI, reads the files without memory of earlier ones, so a name that needs explaining costs every reader and invites misreading.

## WD-031 Lab build after release 1.0

- **Date:** 2026-11-27
- **Decision:** The lab build for memory tiering (WD-018, [lab-build.md](spec/requirements/lab-build.md)) and R-ADP-024 move to after release 1.0. In release 1.0, the tiering rows of the VCF vCommunity Adapter are tested with fakes, and on the physical lab clusters as "not applicable" (R-ADP-014). The lab facts of Q-120 and Q-122 wait until the lab build starts.
- **Reason:** The author, 2026-11-27: "Defer memory tiering lab to be after Release 1.0."

## WD-032 The adapter keeps its vCommunity identity

- **Date:** 2026-11-27
- **Decision:** The management pack keeps its identity in VCF Operations: adapter kind `vCommunity`, display name "VCF vCommunity Adapter", manifest name `iSDK_vCommunity`, key prefix `vCommunity|`, the image `ghcr.io/e1-rahabok/vcf-operations-vcommunity`, the pak name the build makes from them, and "vCommunity" in the names of its dashboards, views and reports. The repository keeps its name, PCM-Adapter. The pack's description explains how it works with Agent E2, PCM and isvara.io. R-ADP-001 to R-ADP-004 are dropped. This replaces the decisions on Q-72 to Q-79 and the parts of WD-007 and WD-016 that renamed the pack.
- **Reason:** The author, 2026-11-27: PCM is a vCommunity project, where VMware vExperts and VMUG members work together, and the name shows a grassroots effort. "Private Cloud Manager" is too long for a key prefix.

## WD-033 Data states in release 1.0

- **Date:** 2026-11-27
- **Decision:** In release 1.0, the VCF vCommunity Adapter publishes no value built from a partial read (R-ADP-018). PCM shows "No data" for a stale value from the time of the value (R-LIVE-015). The state codes, which say why a row or KPI has no value, come after release 1.0 (R-ADP-013 to R-ADP-017). PCM's key list comes from the adapter's module tables, and the lab read checks it (R-ADP-019).
- **Reason:** The author, 2026-11-27, accepting Claude's recommendation. The adapter already leaves a metric blank when its input is older than 10 minutes. A partial read gives values that look normal, which is a correctness bug. The reason for a blank is useful, but release 1.0 is a demo and can show "No data" without it.

## WD-034 Value management after release 1.0

- **Date:** 2026-11-27
- **Decision:** Value management, the fifth pillar of The SP5 Framework (cost, price and business value), comes after release 1.0. Release 1.0 adds no knowledge, KPI or feature for it. Agent E2's files tagged `value` stay as they are, and isvara.io's IT management path shows them under value.
- **Reason:** The author, 2026-11-27: "Value Management is after Release 1.0."

## WD-035 New knowledge forms after release 1.0

- **Date:** 2026-11-27
- **Decision:** Three new knowledge forms proposed for Agent E2 come after release 1.0: workload footprints, investigations over several steps, and "At large scale" notes ([knowledge model](spec/knowledge-model.md), sections Experience and Scale). isvara.io's choice of a small or large estate waits for the notes. Adding the knowledge model to agent-e2's KNOWLEDGE-ENGINEERING.md stays in release 1.0.
- **Reason:** The author, 2026-11-27: "Defer all three to after Release 1.0", on Claude's recommendation. Each form needs new knowledge from the author's field experience, and release 1.0 must stay small enough to finish (WD-026).

## WD-036 What the workspace specifies

- **Date:** 2026-11-27
- **Decision:** The workspace specifies only where the repositories meet: the contracts, the checks that compare both sides, and the workspace's own tools. Domain knowledge, such as a formula, the scoring model or a threshold, lives in agent-e2: its knowledge files explain it and its catalog holds the data rows. How a repository implements something, and the tests of that implementation, live in that repository. A workspace requirement on a contract says that two sides are equal and names the check that compares them. "Comes from Agent E2" means that a value is stated in Agent E2 and that the implementing repository's copy equals it; nothing reads the agent-e2 repository at run time. Dropped by this decision: R-KPI-004, R-KPI-007, R-KPI-008 (moved to R-CONTENT-001), R-ADP-009 and R-ADP-012. Replaces the decision on Q-87.
- **Reason:** The author, 2026-11-27. R-KPI-004 asked the catalog to hold scoring rules, which a catalog of data rows cannot do; the scoring is explained in Agent E2's [performance-kpi-design.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/performance-kpi-design.md) and implemented in the adapter's [kpi_score.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/kpi_score.py). R-KPI-007 and R-ADP-012 restated domain knowledge that Agent E2 already holds.
