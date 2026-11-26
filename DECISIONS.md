# Decisions

Decisions that bind more than one repository. A decision inside one repository goes in that repository's own log:

| Repository | Its decision log |
|---|---|
| agent-e2 | [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) |
| PCM-Adapter | Its issues and pull requests |
| private-cloud-management | [decisions.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md) |
| isvara | [PLAN.md](https://github.com/e1-rahabok/isvara/blob/main/PLAN.md) |

One entry each, newest at the bottom. A changed decision is edited in place; git keeps the history. Each entry has a heading with its ID, the decision, and the reason. "Q-" IDs are the author's answers in the [interview, round 1](spec/interview-round-1.md); other IDs are explained in the [glossary](spec/glossary.md).

## W-001 Agent E2 as the source of domain knowledge

- **Date:** 2026-11-25
- **Decision:** Agent E2 is the source of all domain knowledge: KPI names, parts, limits, scoring, thresholds, flows and explanations. PCM-Adapter implements the KPIs. PCM and isvara.io consume; isvara.io holds no knowledge of its own (Q-15, Q-18). A change to domain knowledge starts in agent-e2.
- **Reason:** With one master copy, every other copy can be generated from it or checked against it ([C1, KPI definitions](spec/glossary.md#c1)).

## W-002 Stage 1 only

- **Date:** 2026-11-25
- **Decision:** Stage 1 only. PCM is a demo in the lab, and Agent E2 uses a cloud model through Vercel AI Gateway. A customer's on-premises deployment with a local model is stage 2 and out of scope.
- **Reason:** A plan that describes two futures at once leads each session to build toward the wrong one. Stage 2 text stays in the child repositories as the target.

## W-003 Synthetic and live demos kept apart

- **Date:** 2026-11-25
- **Decision:** PCM keeps its synthetic ACME demo unchanged and adds a separate live demo as a new entry in the demo drop-down. The two are separate demos, never switched inside one page. Details: W-015.
- **Reason:** The lab has too little activity to show Agent E2; the live demo proves PCM reads real data (Q-20, Q-32).

## W-004 Two web apps sharing Agent E2

- **Date:** 2026-11-25
- **Decision:** PCM (private) and isvara.io (public) are two web apps. Both use Agent E2 for knowledge, through the same Vercel AI Gateway. isvara.io connects to no live system. Agent E2 replaces AskIO on isvara.io.
- **Reason:** Both apps then give the same answers from the same knowledge. Agent E2's model costs less per call than AskIO's, but it holds conversations and reads CSV files and screenshots, so the cost per visitor may rise (Q-I1); the budget is W-014.

## W-005 isvara.io content from the knowledge base

- **Date:** 2026-11-25
- **Decision:** isvara.io's content will come from the Agent E2 knowledge base, not from the Word and Excel files. The guide, the tools and the assessment pages are rebuilt (W-017).
- **Reason:** isvara.io then holds no copy of the knowledge that could drift from Agent E2 (W-001).

## W-006 An exam for people on isvara.io

- **Date:** 2026-11-25
- **Decision:** isvara.io gets an exam for people: 10 short, very hard multiple-choice questions that test depth of understanding, not calculation. A wrong answer loses marks; no answer scores 0. The exam is kept in isvara.io. It is separate from Agent E2's benchmark, which tests the machine.
- **Reason:** A people's exam and a machine benchmark have different purposes (Q-56).

## W-007 PCM-Adapter's new name and identity

- **Date:** 2026-11-25
- **Decision:** VCF-vCommunity-Adapter is renamed PCM-Adapter: the repository, and also the pack's identity in VCF Operations (W-016).
- **Reason:** PCM D-096: the adapter is part of PCM. The author confirmed no installed instance needs protecting (Q-2, Q-I4).

## W-008 Decision logs per repository

- **Date:** 2026-11-25
- **Decision:** Each repository keeps its own decision log. This file holds only decisions that bind more than one repository, plus the index above.
- **Reason:** A cross-repo session needs one place to look; a single-repo session already has its own.

## W-009 Git workflow in the early phase

- **Date:** 2026-11-25
- **Decision:** Git workflow: see [CLAUDE.md](CLAUDE.md), section Git. One branch and pull request per change per repository. While the project is early (defining scope and documentation), Claude merges every pull request itself once the checks pass, and warns the author about a major change in the pull request text and in its report. Revisit when the products have users.
- **Reason:** The author, 2026-11-25: early work is mostly scope and documentation, so waiting for review costs more than it saves. The warning keeps the author aware of what spreads to other repositories.

## W-010 Contract checks in code

- **Date:** 2026-11-25
- **Decision:** Contracts between repositories are checked by code in [`checks/`](checks). A pull request that breaks a check is not merged. Known gaps are a baseline that only shrinks. Every contract has a check (Q-I1).
- **Reason:** Without a check, the two sides of a contract drift apart and nobody notices until something breaks.

## W-011 Lab credentials

- **Date:** 2026-11-25
- **Decision:** Lab credentials. On the author's laptop: two DPAPI files in `$HOME\.secrets\` (`Export-Clixml`), one for a read-only VCF Operations account (reading and validating) and one for the admin account (installing and restarting the pack); the scripts of PCM-Adapter and PCM change to read them. On the PCM lab VM: `/etc/pcm/pcm.env`, root and group `pcm` only.
- **Reason:** Agreed (Q-40). Before this, PCM-Adapter's scripts read an admin login from a file inside the repository folder, and PCM's lab script read Windows Credential Manager.

## W-012 Stage 1 success

- **Date:** 2026-11-25
- **Decision:** Stage 1 succeeds when VMware colleagues and customers who see the PCM demo find it useful and want to fork the repositories privately, to customise and deploy in their own private cloud; when Agent E2 explains a real lab KPI correctly in the live demo; and when every contract is checked automatically.
- **Reason:** The author's answers to Q-I1 and Q-I2.

## W-013 Agent E2 in stage 1

- **Date:** 2026-11-25
- **Decision:** Agent E2 in stage 1: accuracy comes before speed; an answer may take minutes; no streaming, but the user always sees that Agent E2 is still working. Free-text answers are graded automatically by a strong model as judge, as Agent E2's earlier free-text benchmark was. The model is Gemma 4 31B, or a later version when one comes. Every knowledge file is used, drafts included; a review gate on files waits until after go-live.
- **Reason:** The author's answers to Q-I3, Q-5, Q-7 and Q-10.

## W-014 Spending on Vercel AI Gateway

- **Date:** 2026-11-25
- **Decision:** Spending on Vercel AI Gateway is tracked by the author on vercel.com. A benchmark run has a budget of US$100. After isvara.io goes live, it must stay within US$50 a month (the Vercel subscription is already US$40).
- **Reason:** The author's answer to Q-9. The US$50 limit is a roadmap task after go-live.

## W-015 PCM's live demo

- **Date:** 2026-11-25
- **Decision:** PCM's live demo: the L2 workspace only, for performance and capacity management only. Its inventory comes from VCF Operations and starts at the VCF instance; an object's ID is its VCF Operations resource ID. Class of service, region, environment and time zone exist only in the synthetic demo. PCM shows what PCM-Adapter publishes and says "No data" when a value is stale. It reads through with a 60-second cache and stores no metrics. It may compute for display, and never writes to VCF Operations. Lab facts may go to the cloud model. Actions, stories, cases and the calendar are out of 1.0.
- **Reason:** The author's answers to Q-20 to Q-39. Requirements: [spec/requirements/pcm-live.md](spec/requirements/pcm-live.md).

## W-016 PCM-Adapter's scope of change and its rules

- **Date:** 2026-11-25
- **Decision:** PCM-Adapter may change anything, including its adapter kind, manifest name, metric key prefix, image path and pak name. A metric's key comes from the adapter; its name comes from Agent E2's catalog. All scoring logic comes from Agent E2, including the score bands and the closure levels. One Cluster Risk level for every cluster. Usable capacity is Total − HA − Buffer. A metric whose name says "peak" is a 20-second peak; others are 5-minute averages. Data absent by design is made explicit by the adapter.
- **Reason:** The author's answers to Q-I4, Q-1, Q-2, Q-14 to Q-17, Q-19 and Q-28. Requirements: [spec/requirements/pcm-adapter.md](spec/requirements/pcm-adapter.md).

## W-017 isvara.io rebuild

- **Date:** 2026-11-25
- **Decision:** isvara.io is rebuilt: same look and feel, new functionality; the old site goes. Its pages are AI rewrites of Agent E2's knowledge files, with no AI-speak. A cited source opens the knowledge file, with a note that it is written for a model. The injection guard sits in isvara.io, before it calls Agent E2. The "load-and-ask" design retires. Downloads and the weekly Word refresh continue. It is built on a branch with a Vercel preview and switched over in one release. Each feature waits for the author's review in [spec/design/isvara-revamp.md](spec/design/isvara-revamp.md).
- **Reason:** The author's answers to Q-41 to Q-55.

## W-018 Lab build for memory tiering

- **Date:** 2026-11-25
- **Decision:** The physical lab hosts have no memory tiering. The new repository [lab-build](https://github.com/e1-rahabok/lab-build) builds nested virtual ESXi hosts with memory tiering automatically, so tiering features can be tested. Tests run against the live lab from the author's laptop, using PCM-Adapter's tools to install, validate and take screenshots.
- **Reason:** The author's answers to Q-37 and Q-38. Requirements: [spec/requirements/lab-build.md](spec/requirements/lab-build.md).

## W-019 Place for questions across repositories

- **Date:** 2026-11-25
- **Decision:** A question about one repository stays in that repository's question file; a question that binds several repositories goes to this workspace's [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).
- **Reason:** The author's answer to Q-13.

## W-020 No bare short names

- **Date:** 2026-11-25
- **Decision:** No bare short names. A document uses an ID such as C3, W-012 or Q-27 only with its meaning, or as a link to the [glossary](spec/glossary.md), on first use.
- **Reason:** The author could not tell what "C3" meant (Q-46).

## W-021 Agent E2's plan and older benchmarks

- **Date:** 2026-11-25
- **Decision:** Agent E2's plan is rewritten for stage 1, and its older benchmarks are removed permanently.
- **Reason:** The author's answers to Q-6 and Q-12: the outdated material confuses readers and Claude.

## W-022 isvara.io organised by visitor reasons

- **Date:** 2026-11-26
- **Decision:** isvara.io is organised by why its visitors come: to read (articles, books, infographics), ask (Agent E2), listen (podcast), solve (calculators), catch up (What's New), fork (manual), find (search, with regular expressions), practise (Fun Quiz), engage (survey), and download. Each is a door in the header and on the home page; every feature sits behind one. All forms come from the same knowledge files.
- **Reason:** The author's visitor model, 2026-11-26. Plan: [spec/design/isvara-revamp.md](spec/design/isvara-revamp.md), section 4.
- **Status:** a proposal under review. The author shared the visitor model as a suggestion (2026-11-26); the three learning paths discussed since may replace it.

## W-023 Writing rules for people and for machines

- **Date:** 2026-11-26
- **Decision:** Documents for people follow Agent E2's writing rules ([writing.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/writing.md)) and its list of flagged phrases (`avoid_ai_speak` in [rules_check_values.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/rules_check_values.yaml)): plain sentences, no flagged phrases, no slogans or "X, not Y", headings as noun phrases of at most 9 words, short table cells. Documents for machines (the CLAUDE.md files, requirements, templates) are written for an agent to follow: one rule per bullet, exact paths and names, the trigger before the action. The rules stay in agent-e2; [tools/style.py](tools/style.py) reads them from there and checks this repository in CI. The same rules apply to commit messages and pull request text.
- **Reason:** The author has fixed AI-speak in Agent E2 several times (2026-11-26). One copy of the rules, checked by code, keeps every repository consistent.
