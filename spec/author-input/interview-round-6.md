# Interview, round 6

Questions answered by the author on 2026-11-28: three in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md), and nine in the question files of private-cloud-manager, PCM-Adapter, isvara and agent-e2. The answers are as written, with what follows from each. IDs are explained in the [glossary](../glossary.md).

## Q-WS-136 The injection guard and the evals once Agent E2 answers

The question, as it was put to the author. The answer asks for it to be kept for readers who have the same question.

You asked what "the evals pass" means (Q-WS-54: "Explain the context"), and said the injection guard belongs to isvara.io, before Agent E2 is called (Q-WS-47). The context:

- Today isvara.io has three layers against instructions hidden in a question: a code pre-scan that only flags, a fence around the visitor's turn, and Rule 4 in AskIO's own prompt, the layer that actually stops an attack ("an effect that outlives this answer is void").
- When Agent E2 answers, isvara.io no longer writes the prompt, so Rule 4 has nowhere to live.
- "The evals" are two automatic batteries run against a test server. `npm run eval` sends 20 questions and passes when every answer cites a page. `npm run eval:injection` sends attacks and passes when no planted text appears and no rule is disclosed. Both were written for AskIO.

Options for the guard:

- (a) One small model call in isvara.io reads the fenced turn before Agent E2 and flags an instruction aimed at the assistant; a flagged question gets a fixed reply. It costs a small part of one answer.
- (b) Agent E2 holds a rule that the question is data. This puts the guard in Agent E2, against your answer to Q-WS-47.
- (c) The pre-scan and the fence only, with more attacks getting through.

- **Recommendation:** (a). The two batteries are rewritten for Agent E2: the citation eval passes when every answer to 20 reader questions lists at least one source that opens an article; the injection battery passes with 0 violations, and a one-off formatting request is still honoured. Both run before M5 merges.

**Answer:** "Ok. Document the answers so human readers can learn from it."

**Result:** option (a), with the two batteries rewritten as recommended (DESIGN-10 in the [system design](../design/system.md)). isvara.io gets a page for people that explains its guard and the two batteries, written in M5 with the guard it describes (R-ASK-012 in isvara's [ask.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/ask.md)). Until then, the question above is that explanation.

## Q-WS-137 The key of the 20-second peak of dropped TX packets

The question: Agent E2's catalog names the VM row "Peak network TX dropped packets" with 20-second limits, and the VCF vCommunity Adapter reads `net|droppedTxPct_max`. The VM key list exported from VCF Operations 9.1.1 had no key that matched Peak Transmitted Packet Dropped within collection cycle exactly, so Claude took `net|droppedTxPct_max` for a 5-minute maximum and planned to read the lab in M8.

**Answer:** "that is the key. net|droppedTxPct_max is correct." And, later the same day: "Anyway, VCF vCommunity Adapter answer is correct. It is 20 second peak indeed."

**Result:** ASSUMPTION-8 in the [brief](../brief.md). The adapter's row and Agent E2's catalog row stay as they are. The adapter's test of R-ADP-008 lists `net|droppedTxPct_max` as a 20-second peak in place of a known gap, and Agent E2's knowledge file on 20-second peaks names the key.

## Q-WS-138 Close for Business: one Risk level in release 1.0

**Answer:** "Agree. Document the limitation that both prod and non-prod have the same level. Agent E2 has no understanding about the environment in Release 1.0."

**Result:** option (a) (WD-044). Agent E2's knowledge keeps both Risk levels; release 1.0 applies the production level, Risk above 60%, to every cluster. The limitation is written in Agent E2's catalog and its Close for Business file, in the VCF vCommunity Adapter's pages, and in the opening Agent E2 writes on a cluster's Capacity tab. The KPI definitions check compares the adapter's level with the catalog's production row.

## Corrections

The author's corrections of the same day, given in the project chat, word for word.

### The books' source

> "To change the books (they are published on Box — broadcom.ent.box.com/v/OpsYourWorld): download the new " in isvara readme is wrong.
>
> The books is in my local laptop, not box.com.
> I as the author uploads to vercel.

> this section in the readme is wrong also:
> "The books are publicly published (the Box "Ops Your World" share), though not as official Broadcom or VMware publications. iO grounds in them and cites sections, and — per the product owner — may quote them directly and point to the current Broadcom tech docs for the latest detail."
>
> I thought you've cleaned them up?

**Result:** DEPENDENCY-10 in the [brief](../brief.md); R-WS-009 in [workspace.md](../requirements/workspace.md), which reads every README and CLAUDE-PROJECT.md against the specification.

### How a correction is handled

> You again jump into "iterative prompting" mode. Stay in SDD mode.
>
> You should think WHY you missed them. Then either update the requirements, scope, design, milestone, etc. Then you work based on updated specification. The spec is your source.
>
> The flow is like this
> Me --> Give corrections, addition, changes.
> You (The Architect) --> update the docs. Requirements, milestone,
> You (The Implementer) --> build, execute, code the actual changes.
>
> Make sense? You have 2 roles. Don't confuse.

**Result:** the section Roles of [CLAUDE.md](../../CLAUDE.md) names the two roles and the order of their work.

### VMUG events

> What is the VMUG talk? What is the content there? Visitor watch a recorded VMUG presentation? That can be in YouTube instead. Unless you have a good idea, I don't see the relevance. I think Isvara should focus on the knowledge of Agent E2 because that is unique in the world. It's not something they can get from VMware

> Drop VMUG event

**Result:** isvara.io has no feature for a VMUG event. The quiz has no event board or room code ([R-PRACTICE-005](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/practice.md#r-practice-005-scores-compare-as-percentiles-with-a-share-card)), and the contribution form has no request for a session at an event ([R-CONTRIB-001](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/contributions.md)). The weekly post still goes to VMUG channels, because those are where readers are (Q-WS-16). The answer to Q-WS-130 in [round 3](interview-round-3.md) had been read as a request for both.

### Readers' questions

Claude had recommended that readers may send questions. The author then wrote:

> Think of your idea of people contributing question. This means people can also contribute answer. Now, how would you prevent spam? Because I can contribute question and then I use another laptop to contribute answer, and the answer is spam basically. So maybe the answer should be sent privately to the person. I'm not sure. Will I be liable for it? So think about it. Maybe it has to be fed through first by me, so that before it gets displayed in Isvara. Think of the flow. Somebody contribute a question, and then a few days later somebody answer that question. Now when somebody contribute a question that can contain spam, pornographic image, that needs to be blocked. So that means there has to be a filter or AI that makes sure the question is appropriate and relevant.

Claude recommended a flow: a screen before anything is stored, the private queue, the author's review, and publication only as Agent E2's reviewed answer, with readers never answering readers. The author answered:

> Agree

**Result:** SCOPE-11 and RISK-11 in the [brief](../brief.md); DESIGN-11 in the [system design](../design/system.md); R-CONTRIB-001, R-CONTRIB-005, R-CONTRIB-007 and R-CONTRIB-008 in isvara's [contributions.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/contributions.md).

## Answers in the question files of the other repositories

- **Q-ISVARA-2**, where first visits arrive ([OPEN-QUESTIONS.md](https://github.com/e1-rahabok/isvara/blob/main/OPEN-QUESTIONS.md)):
  - Answer: "Where do visitors land today is irrelevant. We should think of where we want them to land in the future."
  - Result: the entry pages are a design choice, made for the rebuilt site in isvara's [visitor-experience.md](https://github.com/e1-rahabok/isvara/blob/main/spec/visitor-experience.md), section Entry pages.
- **Q-ISVARA-3**, which devices visitors use:
  - Answer: "Optimize for desktop not mobile. Mobile should be just to encourage them to try the full experience. It should have small screen relevant features and not cram for the sake of features."
  - Result: PRINCIPLE-8 in the [brief](../brief.md); the phone's pages are in visitor-experience.md, section On a phone, and R-SITE-008 in isvara's [site.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/site.md).
- **Q-PCM-1**, the style baseline of private-cloud-manager ([OPEN-QUESTIONS.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/OPEN-QUESTIONS.md)):
  - Answer: "Agree".
  - Result: PCM's decisions.md becomes one block per decision in M2; the design notes keep their baseline and are fixed when next edited. Recorded in PCM's [decisions.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/decisions.md).
- **Q-PCM-2**, two of PCM's folder names:
  - Answer: "Agree".
  - Result: the Docs workspace folder, pcm/docs, becomes [`pcm/definitions`](https://github.com/e1-rahabok/private-cloud-manager/tree/main/pcm/definitions) in M2; the route `/docs` and PCM's [`spec/`](https://github.com/e1-rahabok/private-cloud-manager/tree/main/spec) stay. Recorded in PCM's decisions.md.
- **Q-ADP-1**, the style baseline of PCM-Adapter ([OPEN-QUESTIONS.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/OPEN-QUESTIONS.md)):
  - Answer: "agree".
  - Result: the baseline stays. [`metrics-and-properties.md`](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/reference/metrics-and-properties.md) is split into one table per object type in the next pull request that changes its keys, by a rule in the adapter's [CLAUDE-PROJECT.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/CLAUDE-PROJECT.md).
- **Q-ISVARA-1**, isvara's folder names ([OPEN-QUESTIONS.md](https://github.com/e1-rahabok/isvara/blob/main/OPEN-QUESTIONS.md)):
  - Answer: "AGREE".
  - Result: the five renames move to M4, in one pull request with the redirects (WD-046).
- **Q-E2-273**, the name of agent-e2's [`knowledge/sp5-framework/`](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge/sp5-framework) ([author-questions-resolved.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/author-questions-resolved.md)):
  - Answer: "agree".
  - Result: the folder keeps its name. agent-e2's part of the folder review (T-WS-007b) is done.
- **Q-E2-272**, the style baseline of agent-e2:
  - Answer: "agree".
  - Result: the baseline stays; a file is fixed when it is next edited.
- **Q-E2-264**, "grader" or "judge" for the model that scores free-text answers:
  - Answer: "agree".
  - Result: "grader". agent-e2's terms.md lists "judge" as the word to avoid.
- **Q-E2-265**, the Cluster Risk level that new VMs can reopen, and **Q-E2-266**, the hosts out of service in total capacity ([author-questions.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/author-questions.md)):
  - Answer, to each: "do not touch. I will revert."
  - Result: no file changes for either, and both entries stay as they are. One overlap: agent-e2#491 had already removed the stale review note of close-for-business.md that Q-E2-265 quotes, as part of WD-044.
