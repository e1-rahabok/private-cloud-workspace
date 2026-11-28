# Interview, round 6

Questions answered by the author on 2026-11-28: four in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md), and thirteen in the question files of private-cloud-manager, PCM-Adapter, isvara and agent-e2. The answers are as written, with what follows from each. IDs are explained in the [glossary](../glossary.md).

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

## Q-WS-139 Whether PCM runs as a container in release 1.0

The question: the brief said "PCM runs as a Linux container, with VKS integration", while the system design and PCM's deploy/README.md run PCM as a service on a Linux VM in the lab, and no requirement builds a container. Asked during the fresh review of R-WS-009.

**Answer:** "PCM is already running in a VM in the lab. [the address of PCM's L2 capacity page on the lab VM] is PCM." The address is left out here: it is a private address in the author's lab.

**Result:** SCOPE-3 in the [brief](../brief.md): in release 1.0 PCM runs on the Linux VM in the lab, as the system design says. The Linux container with VKS integration is listed under SCOPE-19, after release 1.0.

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

### Credit for contributors

> How would you acknowledge when someone genuinely contributes? For example, should we have their names, their LinkedIn profile, their company? How to encourage the community building? And should it say their country because you can detect the IP address? Is it a good idea at all? Research other online community places. Reddit is a bad example as people identity cannot be verified at all. LinkedIn is much more civil

Claude recommended credit by name and one profile link, on request; no company and no country; credit on the article, in What's New and on a contributors page without ranks; tags in the weekly post with consent; and a badge. The author answered:

> Agree

**Result:** DESIGN-11 in the [system design](../design/system.md); R-CONTRIB-001, R-CONTRIB-005, R-CONTRIB-007 and R-CONTRIB-009 in isvara's [contributions.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/contributions.md).

### Lab addresses in GitHub

> PCM is already running in a VM in the lab. https://<the lab VM>/l2/monitor/compute/SG-S-01/capacity?now=2026-10-19T10%3A05%3A00%2B08%3A00&window=24h is PCM.
>
> BTW, why did you put all the IP addresses in GitHub? While they are all private, behind my VPN, shouldn't you mask it? Where do you store password, secrets?

The lab VM's address in the link is replaced by its role, by the rule this answer set.

**Result:** DESIGN-9 in the [system design](../design/system.md) keeps the lab's addresses and host names in `$HOME\.secrets\lab.json` and `/etc/pcm/pcm.env`, never in a repository; R-WS-010 in [workspace.md](../requirements/workspace.md) and its check enforce it in all five repositories. The history is not rewritten (DESIGN-9, rejected option f).

### Security as the architect's work

> Why did you wait for me for the security on the IP address and host name? Shouldn't this be part of your professional application development role as an experienced software architect? Is there anything else that you need to consider? Remember the SDD mode.

**Result:** DESIGN-24 in the [system design](../design/system.md) reviews release 1.0 against four public baselines, mapped item by item in its section Security baseline; DESIGN-25 to DESIGN-27 add dependency updates, secret scanning, least rights in workflows, and recovery. R-WS-011 to R-WS-013 in [workspace.md](../requirements/workspace.md) and their checks enforce them in all five repositories. ASSUMPTION-9 and RISK-12 are in the [brief](../brief.md); R-PROTECT-007 and R-PROTECT-008 are in isvara's [protection.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/protection.md). R-LIVE-037 in private-cloud-manager's [live-demo.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/requirements/live-demo.md) closes the lab VM to everything but TLS and SSH from the VPN, and keeps it patched; the author approved closing port 8080 ("Go ahead and close port 8080").

### Branches

Asked to read Q-PCM-4 while every repository listed branches other than `main`:

> I'm unable to find the folders. Also, there are many branches ahead. This is impossible to review.

On three branches listed for deletion that were ahead of `main`:

> But they are ahead. Why are they ahead? Normally we delete only if they are not ahead.

On four branches, none ahead of `main`, left for the author to delete by hand:

> This is a common problem. Find a solution as we're in SDD mode.

**Result:** CONSTRAINT-9 in the [brief](../brief.md) states that a cloud session cannot delete a branch. DESIGN-28 in the [system design](../design/system.md) deletes every branch that is not ahead of `main` inside GitHub, with each repository's own token, and keeps every branch ahead of it. R-WS-014 in [workspace.md](../requirements/workspace.md) and its tests enforce it in all five repositories, and the workspace's [CLAUDE-PROJECT.md](../../CLAUDE-PROJECT.md) no longer asks the author to delete branches.

### isvara.io's folders, visitors and wireframes

> I think you should review the Agent E2 properly.
>
> The folder structure is still confusing. I'm unable to guess what those top level folders are for.
> For examples:
>
> * app = what application, since the whole isvara.io is an application? It has a dozen or so subfolders. From the name, I'm unsure. For example, estate means screen real estate? homelabs can be removed as it's no longer required. Design the folder properly. Maybe you need additional layer of folder hierarchy?
> * components = The English word components means parts. Maybe you need 2 words so it's easier?
>
> Think of the Visitors and why they come.
> How do you serve first time visitor and repeat visitor? Can repeat visitor bookmark certain page directly? How do you know someone is first time or not if they simply lands at the home page?
>
> The Agent E2 visitor experience is shown in ASCII art. It is hard to guess what you intend to build. As a UX professional, how will you convey the mock to minimize surprise. I don't have to know the details. Just high level rough sketch that has better screen alignment that ASCII art will do. It can be SVG or whatever. You know better. Again, as The Architect you update the spec, so The Implementer can execute.

The folders the author names are isvara's, the site that is rebuilt on Agent E2.

**Result:** DESIGN-6 in the [system design](../design/system.md) now designs names for a reader who knows the field but not the framework, and T-WS-007b in [workspace.md](../requirements/workspace.md) reads the tree that way. R-REPO-010 in isvara's [clean-up.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/clean-up.md) sets isvara's layout, mapped in its README; R-REPO-011 removes Homelabs. isvara's [visitor-experience.md](https://github.com/e1-rahabok/isvara/blob/main/spec/visitor-experience.md) adds the first visit and the return, and the addresses to bookmark, with R-SITE-009 and R-SITE-010 in its [site.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/site.md); its text art is replaced by SVG wireframes drawn from one list of parts and checked in CI.

Two replies on the result, the same day:

> evals/ → ask-io-tests/
>
> Why AskIO? It will be 100% gone. No more. Agent E2 replaces it. I've said this multiple times.

> Homelabs is deleted, and /homelabs redirects to /tools.
>
> if deleted, why redirect? That homelab serve no purpose anymore. Completely delete it

**Result:** R-REPO-010 now refuses a folder named after a part the roadmap removes: AskIO's code is [`site-logic/answering/`](https://github.com/e1-rahabok/isvara/tree/main/site-logic/answering) and its tests are [`answer-tests/`](https://github.com/e1-rahabok/isvara/tree/main/answer-tests), and isvara's folder check fails on such a name. R-REPO-011 now has `/homelabs` answer 404, with no redirect; R-SITE-010 in isvara's [site.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/site.md) says a page removed with nothing to cover it answers 404.

### isvara.io's deployment

On being asked to approve a merge described as deploying isvara.io:

> As in deploy live in production? How can it be? The website is based on another repository, which I forked. You're updating the fork.
>
> We will not replace a live site until its fully tested. Your eagerness to update a website visible to the world is worrying. We need to make sure the spec is 100% correct first.
>
> Here is the process:
>
> 1. We finalize the spec
> 2. We deploy to a parallel site. Give it a name.
> 3. The site goes live. Nobody will basically know as it's not advertised. I will then compare side by side.
> 4. Only when I'm satisfied, we replace the old site.
>
> Make sense?

Which Vercel account serves isvara.io today:

> agentisvara-4524

(The account's email address, also given, is left out of the repository.) A screenshot the author sent next shows the live project `isvara` in the Vercel team Agent ISV (`agent-isv`), with the author's own account `iwanang-1023` a member:

> iwanang-1023 has access. See screenshot. You should login and check for yourself as you're in SDD mode.

Whether the fork is connected to a Vercel project:

> I don't think so. As The Architect, design the deployment architecture, document it. When done, ask The Implementer to read and set up.

Once the parallel site was up, on whether it should ask visitors to sign in:

> It does not ask to sign in. I'm good with it as the real one hardly has any visitors.
>
> What do you mean compare? It's the old content.

> No need sign in. As The Architect, have you updated the spec?

**Result:** CONSTRAINT-10 in the [brief](../brief.md) and DESIGN-29 in the [system design](../design/system.md): the parallel site `isvara-next` in the same Vercel team, not indexed and with its own stores, and a switch-over that merges the fork into the original after the author's approval. isvara's [deployment.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/deployment.md) holds R-DEPLOY-001 to R-DEPLOY-004; ROADMAP M2 sets the parallel site up and M7 switches over. The parallel site needs no sign-in, and the comparison with isvara.io starts when it holds new content, because until then it shows the old content.

### Who speaks to the author

On an offer to fix a page test, run the project's own tests on every change, run three reviews and correct the roadmap's ticks in a new thread:

> Is this The Architect asking me? The Implementer does not talk to me. If this is The Architect, what do you need from me as I have no idea what you're talking about. You ask me requirements, scope, etc. Jargons like LPG and CI are aliens to me as I'm not a software developer. I'm just a vibe coder.

**Result:** the brief's section [Users](../brief.md#users) says who the author is and how Claude speaks to the author. CLAUDE.md, the same in all five repositories, says that only the architect speaks to the author, to ask for input or to report a result, and that a reply names each thing by what it does, with no IDs, abbreviations, tool names or file paths unless the author must open the file.

### The milestone review page

On being asked to approve M2 from its review page, which listed each requirement as one short line with its number of tests:

> It's impossible to review because each line is just a short sentence. Not enough context. Plus, it's written for The Implementer, not me. The texts at the end "Tests: 2 anywhere, 0 lab." is irrelevant to me right? You should test properly as you deem appropriate. You can definitely ask me for requirements, scope, etc.

**Result:** R-WS-015 in [workspace.md](../requirements/workspace.md) and DESIGN-30 in the [system design](../design/system.md): the review page tells the author in plain words what the milestone set out to do and why, what changes, what the author is asked to confirm, what was left out and what could go wrong, and says in one line that Claude tested it. It has no test counts. DEPENDENCY-1 in the [brief](../brief.md) names what the page holds.

### Merging pull requests

On a card that asked whether to merge the pull request with the new review page, after the same merge had been blocked once by the session's permission mode:

> As The Architect, you should not ask me for merging, as I don't know the branch details. You should auto merge. With me, focus on requirements, scope, goals.

**Result:** the brief's section [Users](../brief.md#users) says Claude never asks the author to merge, to look at a branch or to delete one, and the workspace's [CLAUDE-PROJECT.md](../../CLAUDE-PROJECT.md), section Several repositories, says Claude merges its own pull request once its checks have passed, without asking. It extends the approval of 2026-11-25, which that file recorded for the early project only.

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
- **Q-PCM-3**, how the author shows the live demo ([OPEN-QUESTIONS.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/OPEN-QUESTIONS.md)):
  - Answer:

    > PCM Live Instance.
    > Since it's connected to a live VCF Operations, it shows the actual VCF inventory. Same structure and UI as the synthetic demo, except the data is live.
    >
    > PCM Demo: Live instance demo.
    > The follows the same as the L2 Specialist.
    > 1. Select a vSphere Cluster. In the lab, there is only 1.
    > 2. The default summary tab appears. I'd ignore this in Release 1.0
    > 3. I'd click the Performance tab.
    > 4. The same content as L2 Specialist demo appears, except the data is live
    > 5. I clicked the larger Agent E2 icon at the top right hand corner
    > 6. The default OOTB questions must be relevant.
    > 7. I clicked on each of them, verifying their answer is correct. The answer is coming live from Vercel the AI gateway, just like in synthetic demo. No difference at all.
    > 8. I click the small Agent E2 icon on the Performance trend chart.
    > 9. The default OOTB questions must be relevant.
    > 10. See step 7 as I'm just repeating.
    > 11. I click every single small Agent E2 icon. Repeat the test.
    > 12. I click the Capacity tab. I repeat step 5 - 11.
    > 13. I select one of the ESXi.
    > 14. This time, I only do Performance tab. No capacity tab needed.
    > 15. I select one of the VM in the ESXi.
    > 16. This time, I only do Performance tab. No capacity tab needed.

  - Result: the live demo opens an object on its Performance tab, with no Summary tab (R-LIVE-004). R-LIVE-036 walks the script: the cluster's Performance and Capacity tabs, then the first host and its first VM, worst first, Performance only, with every Agent E2 mark and every suggested question. "Relevant" and "correct" became tests: R-LIVE-038 checks each suggestion against Agent E2's own rule for the page's situation, R-LIVE-039 checks each answer's figures against the reference script and grades it, and the author rates every answer at the M8 rehearsal. R-LIVE-040 covers Agent E2 or the gateway failing mid-demo. The script is in PCM's [demo/README.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/demo/README.md), section The live demo; the synthetic walk runs now as LPG-31 and LPG-32. The answer does not open VCF Operations beside PCM, so the numbers are compared by the reference script (R-LIVE-024).
- **Q-PCM-2**, two of PCM's folder names:
  - Answer: "Agree".
  - Result: the Docs workspace folder, pcm/docs, becomes [`pcm/definitions`](https://github.com/e1-rahabok/private-cloud-manager/tree/main/pcm/definitions) in M2; the route `/docs` and PCM's [`spec/`](https://github.com/e1-rahabok/private-cloud-manager/tree/main/spec) stay. Recorded in PCM's decisions.md. Q-PCM-4 below renames the folder again.
- **Q-PCM-4**, what PCM's users call the /docs workspace. The question: a fresh reader of PCM's folder tree (T-WS-007b) took [`pcm/definitions`](https://github.com/e1-rahabok/private-cloud-manager/tree/main/pcm/definitions) for the KPI definitions; what do the people who use `/docs` call it? The working assumption, as the author was shown it: "I'm assuming "Docs", so the folder would become pcm/docs-workspace."
  - Answer: "OK".
  - Result: the folder is [`pcm/docs_workspace`](https://github.com/e1-rahabok/private-cloud-manager/tree/main/pcm/docs_workspace), with an underscore: the folder is a Python package, and Python cannot import a name with a hyphen. Its route stays `/docs`. Written in R-REPO-008 of PCM's [clean-up.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/requirements/clean-up.md), with a new rule that no folder is named with a term that the glossary or the contracts give to something the folder does not hold, and in D-135 of PCM's decisions.md.
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
- **Q-PCM-5**, whether visitors of the public PCM demo ask Agent E2 live questions:
  - Answer: "Yes, look at Ask.io today at isvara.io. It is already answering live question. That's why I said it got spam."
  - Result: yes, with limits against spam and cost: R-PUBLIC-003 in PCM's [public-demo.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/requirements/public-demo.md).
