# 16. Case study log

What happened while this workspace was set up, in order, mistakes included. It covers six days in November 2026.

## The system

Four repositories make one product:

- **Agent E2**, a knowledge service that answers like a VMware performance and capacity expert. It has no user interface.
- **VCF vCommunity Adapter**, a management pack that computes performance and capacity scores inside VMware's monitoring product.
- **PCM**, a web app for operations teams that shows those scores and asks Agent E2 to explain them.
- **isvara.io**, a public learning site that will also use Agent E2.

All four were built with AI over several months, through thousands of small conversations. A fifth repository, for building a test lab automatically, was added along the way.

## Day one: the map and the first checks

**The question.** The author asked whether a long chain of dependent tasks was a reasonable thing to give an AI, given that the goals felt too abstract to work as instructions. The answer was yes, provided each goal is turned into something checkable and the points where the repositories meet are checked by scripts.

**The survey.** The agent read the four repositories. Two were already well specified; one had over a hundred numbered decisions. The gaps were between the repositories: an almost empty parent repository, no list of interfaces, decisions kept in three different places, and rules that contradicted each other.

**Corrections.** The agent's first account got four things wrong:

| The agent said | What was true | Why it was wrong |
|---|---|---|
| The knowledge service's cloud model conflicts with its "local model" goal | The cloud model is for the demo; the local model comes later | The parent repository did not say so |
| The management pack is a separate product | It is part of PCM | One repository's decisions said so; the parent's documents did not |
| PCM will switch from demo data to live data | It keeps both | It had never been written down |
| Publishing exam questions would spoil a benchmark contest | The author did not care about contests | The agent assumed a goal the author did not have |

Each correction went into the decisions and the map.

**Decisions and checks.** The author answered six questions in a few words each. The agent wrote two checks and broke something on purpose to prove each could fail. The first, comparing performance definitions across two repositories, found a real gap on its first run: 11 metrics named differently in each place.

## Day two: the interview

**The agent skipped its own advice.** With the files merged, the agent proposed starting the first build. The author stopped it with three questions: is the interview done? Are the requirements written so they can be tested? Are the stop conditions in place? The honest answers were no, no, and partly. Six questions in chat had been called an interview, and the milestones were bullet points. The agent had slipped back into building first and asking afterwards.

**The interview, done properly.** Four agents surveyed the four repositories in parallel for conflicts, undecided items, unstated assumptions and missing requirements, each finding linked to the lines that showed it. About 80 findings became 61 questions, each with a recommendation and an empty answer line for the author to fill in on GitHub.

**Conventions missed.** The author's own repositories already made every file reference a clickable link and drew every diagram as an SVG with its text underneath. The agent had read them and still wrote plain paths and text drawings. Both conventions now have a script that enforces them.

**The answers.** The author answered nearly all 61 questions in one evening, mostly with "Agree", and corrected several assumptions: the live demo is a separate demo of a single role; the management pack may change anything; the public site is rebuilt from scratch.

## Day three: the specification, and how to think

**The specification.** The four survey agents, which still held their context, drafted the requirements for their own repository in parallel: 105 requirements with 176 test scenarios, each citing the answer it came from. A script confirms every requirement has a source and a test. Writing them raised 66 new questions, smaller and more precise, which became the second round.

**A self-inflicted loss.** While gathering those questions from six new files, a script of the agent's rewrote the files before saving what it had collected, and the save failed. The files had not been committed yet, so git could not restore them. The agent rebuilt the questions from what it had read earlier. Commit drafts early.

**A suggestion taken as an order.** The author shared a table of reasons why people visit the public site. The agent recorded it as a decision, rebuilt the site plan around it, added six features and merged it within the hour. The author's reply: you are behaving like a doer; I need a thinker; that was a suggestion. When the agent then thought it through, it found real weaknesses in the table and said so. The author answered with a better idea, three learning paths that overlap, and the design came out of that exchange.

**A question it should have answered itself.** Asked where four topics belong among the learning paths, the agent put the question back to the author, although the answers are basic knowledge in the field. The author pointed this out. Questions are for judgement; the rest the agent decides and states.

**Round three.** The last questions only the author could answer went out in the open-questions file. Two answers taught the agent something about asking:

- One question asked whether the run queue in the guest operating system is counted per vCPU or for the whole guest. The author was unsure. The agent's own knowledge base already held the answer. It should have looked there first.
- Another offered "birds-of-a-feather sessions" at events. The author replied: "not sure what you mean here. We have VMUG event." The jargon cost a round trip.

A third answer was "will supply later. remind me." Those questions stayed open with a trigger: the agent asks again when the milestone that needs them starts.

**The trust question.** Discussing AI-written public content, the author noted that keeping an expert site credible is not a new problem. The discussion that followed became [chapter 15](15-trust-in-ai-written-content.md): separate a wrong source from a wrong rewrite, spend scarce review time on disagreements and on the most-read pages, and build a community that can review.

## Day four: names, and the plan against intent

**Names first.** Early that morning, in short sessions, the author asked for names that explain themselves ([chapter 14](14-names-and-vocabulary.md)):

- "Stage 1" and "release 1.0" meant the same scope. The plan now says release 1.0 for the goal and milestones for its steps.
- Milestones had been numbered in the order they were added, so the roadmap read M2, M8, M9, M10, M3. They were renumbered in the order of work, across 16 files.
- Decision IDs W-001 to W-029 became WD-, for "workspace decision": 208 references in 26 files.
- A new decision made names guessable everywhere, and folders in the web app's repository will be grouped by workspace instead of by phase, so one folder holds the context of one task.

The author's reason fits on one line: "The best documentation is No Documentation."


**The plan had grown.** The session opened with the author's own summary of release 1.0: rebuild isvara.io, add the live demo to PCM, and leave Agent E2 and the management pack nearly untouched. The agent compared it with the roadmap. The files said otherwise: 19 requirements for Agent E2 and 24 for the management pack, in three milestones that the live demo and the site depended on. Each requirement had a source. Together they made a release larger than the author meant, and nobody had noticed. The author then went through the plan item by item.

**Purpose questions shrink a plan.** "What is the grader for? The quiz is multiple choice." The grader scored Agent E2's free-text answers, which the quiz never uses. Once its purpose was stated, the author kept it at 15 questions instead of 40 and moved the rest to the plan after 1.0. The same kind of question cut the management pack's data states to one correctness fix, and moved a lab build, value management and three new kinds of knowledge to after 1.0. Each deferral became a decision with a line under "After release 1.0", so nothing was lost.

**A number taken from a test.** Explaining the progress display, the agent said the caller checks every 2 seconds. The author asked whether that was too often: a VMware administrator knows this is no general chat and does not mind 10 seconds. The 2 seconds came from a test scenario. No requirement set the interval at all, and that gap was the real finding. The person's knowledge of the user set the number.

**The copy that drifted.** The new site plan listed the IT management topics as availability, performance, capacity, configuration and security. Agent E2's tag listed availability, performance, security, capacity and value. The agent proposed a new "configuration" tag in Agent E2 to match the plan. The author's answer: Agent E2 is correct; it is what the framework documents. The newer design document had drifted from the master. The agent should have read the framework before proposing to change it.

**Names carry identity.** In an earlier round the author had let the agent decide the management pack's new name and key prefix, and the agent chose "PCM". The author reversed it: the pack is a vCommunity project of vExperts and VMUG members, and its name shows a grassroots effort. In the same exchange the agent suggested renaming the book to match the software. The author explained the difference. The book, Private Cloud Management, is the discipline. Private Cloud Manager and isvara.io are two applications built on it, for the same audience and different uses.

**A question with no context.** The agent asked: "Should isvara.io treat `what-to-set` files as configuration, with no Agent E2 change?" The author could not tell what it meant. It named a file type the author had never needed to know, gave no link, and had already been settled by the decision on the topics. [Chapter 5](05-the-interview.md)'s rule was in the files. The agent broke it while summarising many items at once.

**Many decisions in one conversation.** The session changed the plan seven times in a few hours. Each change became its own pull request, and several touched the same lines of the roadmap, so two of them conflicted. The agent built the later ones on top of the earlier ones. Merging the last pull request merged the whole stack.

**"Part of", and a Level 100 question.** Another session audited the management pack and reported six names for it, adding that the repository name "suggests it is part of PCM, which it is not". The agent relayed that sentence to the author as a contradiction and asked: "is the adapter part of PCM?" The workspace already answered it. Three files recorded the author's earlier answer, and the contract file described the mechanism: the adapter computes the KPIs inside VCF Operations, and PCM reads them through the Suite API. The author's reply: technically, PCM never connects to the adapter; functionally, PCM's live scenario has no data without it. "Part of" had two meanings, and the agent used the word without saying which. The author asked what else the agent might not know. The relation is now written by mechanism in [SYSTEM.md](../spec/design/system.md), and the working rules say: search the files before asking, verify an audit's claim before relaying it, and describe a relation by mechanism.

**The workspace in the wrong territory.** Asked to approve milestone M2, the author pointed out two problems. The first was the approval itself: its requirements were spread over four files, and approving meant reading each one and its numbers. The second was worse. A requirement said the scoring rules were "defined once, in the catalog, with worked examples". The catalog is a list of data rows: one row per metric with five limits. The scoring model is explained in Agent E2's knowledge and implemented in the management pack's code, and nothing reads the other at run time. An earlier session had turned the author's answer "all their logic should come from Agent E2" into a storage mechanism, without reading the code. Two more requirements restated a capacity formula that Agent E2 already held. The fix was a rule about territory: the workspace specifies only where repositories meet, Agent E2 holds the domain knowledge, and each repository specifies its own implementation. A generated review page now lists each milestone's requirements on one page, one line each.

**Asking for approval too early.** With the review page built, the agent asked the author to approve milestone M2. The author asked why it had jumped to M2 while M1 was unfinished. Approving M2 was the last item of M1, and four items above it were still open: requirements to update, isvara.io's requirements to write, the files to check against the new territory rule, and the milestones to renumber. Any of them could still change M2. The agent had read the line it wanted and skipped the checklist around it.

**The lesson log.** At the end the agent reported that nothing was outstanding. The author asked whether this tutorial had been updated with the session's lessons, "or you forget about it, again?" It had not. Updating this log is now a rule for the end of every session in the agent's working rules ([CLAUDE.md](../CLAUDE.md)).

**The cold-read audit, answered.** A fresh session read the five repositories the way a newcomer would and listed the names it could not guess. The author's answers sorted its findings. Two were already settled: WD-032 had decided the management pack's name, and agent-e2's benchmark questions keep a file name and a separate ID on purpose, which agent-e2's documentation says. Others became changes across all five repositories: question IDs that name their repository (Q-WS-, Q-E2-), releases defined only in the workspace, milestones renumbered in the order of work, no hand-written counts, and every child README linking the workspace. The audit also misread one name: `story_m5` holds PCM's demo story M-5, which the audit took for milestone 5.

## Day five: the milestones rebuilt

**The request.** The author asked for a fresh look at the five repositories and logical milestones: "M0, M1, M2 today overlap. M5 and M6 seems to be just 1 milestone." and "A project first milestone is called Milestone 1." The agent surveyed every repository, then asked three questions before the author left for several hours: may it approve M1 itself after a self-review, which goal comes first, and what to do with tests that need the lab. The author delegated M1's approval only, put isvara.io before the live demo, and accepted lab tests reported as not run.

**What the count showed.** A script counted which milestone each requirement belonged to. 26 of the 32 live demo requirements belonged to none, and two Agent E2 requirements belonged to two. The roadmap also ran two milestones in parallel while the gate allowed one open milestone. Each problem had been invisible because each file read well alone. Both counts became checks.

**One milestone for the lab.** Tests that need the lab sat in three milestones. The laptop that reaches the lab is not offered to cloud sessions, so each of those milestones would have stayed open until a lab session. They moved, unchanged, into new requirements of the live demo's milestone, and the review tool now fails when a lab test sits elsewhere.

**Requirements where their code lives.** The workspace had kept requirements on each repository's own code, against its own decision WD-036. They moved to each repository, and the workspace's tools now read all five. The private isvara repository cannot be read by the workspace's CI, so its pages are reported as not run there and checked by the local run.

**A request half answered.** In round 1 the author asked for a document of isvara.io's before and after, to review before anything was built. A plan of the new site existed, and the request had been treated as answered. The before-and-after document was written in this session, and the first isvara.io milestone now waits for the author's review of it.

**Two claims checked late.** The first draft of that document said the health check's four counters would be scored against catalog rows, and that the super metric builder's keys came from the catalog. Neither was in the catalog. A read of the catalog before publishing caught both.

**A commit with a failing check.** The agent ran every check in a loop that printed the results and then committed, and one style failure went into a commit. A script that exits with a failure now runs before every commit, and the commit only follows a pass.

**Five reviews before approval.** The author delegated M1's approval on one condition: a fresh agent's cold read finds no contradiction. Three cold reads and two checks of the fixes ran in turn. The findings fell from 23 to about a dozen, then to six, then to one stale word. Each round of fixes brought contradictions of its own: a rule added to one repository's project file contradicted the shared stop rule, and two status lines credited a source with a number it did not give. The check after each round caught them.

**An answer quoted where the rule lives.** The author's answer on lab tests sat in the session's record, and the files only paraphrased it. A later session reading the shared stop rule would have stopped at the first change to the adapter's code. The decision now quotes the answer, and the project file cites the decision.

## Day five, continued: M2 in parallel

**An empty milestone.** M2 opened with no work items, and the gate reported "no open item; ask the author to approve", which would have sent a session to ask for the approval of work not yet done. The first pull request of each milestone now writes its items.

**Three helpers, one branch each.** Every repository has one session branch, so two writers in one clone collide. The clean-up of PCM, of agent-e2 and of the adapter's names went to three helper agents, one repository each, while the lead worked in the workspace. A helper opened its pull request and the lead merged it after running the checks again.

**Contract changes in three steps, across four repositories.** The KPI definitions check moved from matching rows by name to matching them by key: first the catalog's key column, then the check, then the renamed rows and the adapter's labels together. The check of contract C3, the Agent E2 API ([glossary](../spec/glossary.md#c3)), moved with PCM's new folders the same way: PCM kept the old path, the check moved, the old path went. A CI run that started a minute before step 2 merged failed for that reason alone; one re-run passed.

**Checks that caught their author.** The new name check failed on its own first file name, `old_names.py`. The new forbidden-names check found a stale link no review had seen. A baseline kept in the workspace would have stopped a child's fix from passing, so each repository keeps its own.

**A rule against itself.** A requirement said "the catalog holds one Risk level for every cluster". Agent E2's knowledge keeps two levels and says to keep them apart. The requirement had read more into the author's answer than it said, so the comparison waits for a question.

**A check narrower than its test.** A cold review of M2 by a fresh session found PCM's old test paths still written in two files. The forbidden-names check matched only links to PCM's old folders, while its test scenario asked for every old path. The check now also matches the paths written out, and a planted break keeps it so. The same review found ROADMAP lines and requirements that said more than the files showed, such as a ticked line whose renames still waited for the author; each was reworded or unticked.

**Eleven answers on one day.** On 2026-11-28 the author answered eleven questions across the five repositories, most with one word, two with "do not touch. I will revert." The first six were recorded in the parent first, as round 6 with three decisions, because the children's requirements cite them. One answer, on the Cluster Risk level, removed a flag from the knowledge service's API that no caller had ever sent. Another asked for the explanation behind a question to be kept for readers, so the record kept it whole. A helper agent took the two answers that changed only the product repository: one block per decision in its log, and a folder renamed for what it holds. It found two things the plan had missed: the specification check read the decision log's table, and nine links in the interview records pointed at line numbers that the new layout moved. The records' links were pinned to the commit before the move, so they still show what the author read. A last fresh review read every Markdown line added in the milestone, across about 170 files, for IDs used without their meaning. It found 4, and a gap in the glossary: three question prefixes no row explained.

## Day six: the method corrected

**The correction.** On 2026-11-28 the author looked at the workspace's folders and wrote that the work was still not spec-driven development: "You record all decisions in DECISIONS.md. This makes you take my decisions as the authority, and then jump into execution. Decision is yours, not mine. I give the input and knowledge as I'm the expert and the user." The workspace had no test plan, and no design of the system as a whole. The author asked for both, for documents to write together (the test plan, acceptance criteria, risks, dependencies and the glossary), and for the agent to design security, scalability, performance and maintainability: "Show me so I can learn." The message ended: "Do not jump to make changes. We need to get this SDD properly done so we can automate."

**An answer that defended the file.** Earlier the same day, asked why DECISIONS.md was needed, a session had answered by mechanism: the specification check reads it, most requirements cite it, and one decision is the source of many requirements. The facts were right, and the answer still missed the point. It argued from what the tools needed, while the author's point was about who decides. Its count was also short: it found nine requirements resting on WD-001, and a count across all five repositories found twelve.

**What the log held.** Sorted by kind, the 46 entries mixed scope, requirements, constraints, design choices, and rules the agent's working files already held. One entry, WD-015 on PCM's live demo, held five kinds in one paragraph ([chapter 2](02-the-method.md)). Each kind has a home in the specification, next to what it shapes.

**Questions that asked for the wrong thing.** The interview records showed the same pattern from the other side. Many questions had asked the author to choose: a stale limit of 15 minutes, one of three designs for the injection guard. The author's most useful answers were input anyway: "No need to wait 15 minutes", and "Document the answers so human readers can learn from it." The interview now asks for input and states the assumption the agent works on meanwhile ([chapter 5](05-the-interview.md)).

**Two threads at once.** One thread restructures the workspace: a brief with the goals, scope, principles, constraints, assumptions, risks and dependencies; a design with its choices and the options each rejected; a test plan; and the decision log retired in three steps, so every check keeps passing on the way. This tutorial follows it in a second thread, in its own folder. The two agreed an order before either wrote: the restructure moves its files first and fixes the tutorial's links to them, and the tutorial's rewrite is built on top, so neither rebases the other's work.

**The second pass.** The tutorial's chapters were drafted while the brief and the design were still being written, so their examples came from the files that were about to move. Once the restructure's first pull request landed, every example was checked against the new files, and six had moved. The failure statements of the old intent file had become the reasons of GOAL-3 and PRINCIPLE-2. The risk examples had a real register to come from, with an ID, an effect, what reduces it and who acts. A cost worry first written as a risk was an assumption in the brief, ASSUMPTION-4, with a check planned for M5. The requirement example gained the new order, Why before Source. The traceability example moved to the workspace's own R-WS-003, since the child repositories' requirements had not yet moved to the new form. And a credentials file described as root's turned out to be readable by a group as well.

**Effort.** The author asked for a high reasoning effort for this work. The project's main chat runs at a fixed low effort, so the deep work went to the threads, where the effort can be raised.

## Lessons

- The agent's first survey was useful precisely because it was wrong in places. Each error pointed to a missing document.
- The author's time went into answers and decisions instead of explaining the system again.
- A check written in an afternoon found a real gap on its first run.
- An agent drifts back to building first even after writing down the method. A short question from the person, such as "is the interview done?", brings it back.
- A convention the agent has read about is not a convention it follows. Only a script makes it hold.
- Most answers can be one word when each question carries a recommendation.
- A specification raises its own questions. Expect a second round.
- The agent is most useful when it argues. The best design idea in this log came from the author, in reply to the agent's critique of the author's first idea.
- Look in your own knowledge base before asking the person. Use their words in a question, without jargon.
- A question that can wait gets a trigger: the milestone or event when it is asked again.
- A name that needs explaining costs every session. Rename it everywhere, and let the checks catch what the renaming broke.
- Compare the plan with the person's intent at the start of each release. Requirements with good sources can still add up to a release nobody asked for.
- Ask what each planned item is for. An item whose purpose takes more than a sentence to explain is a candidate for later.
- A deferral is a decision, with its own line in the plan after the release.
- When two documents disagree, find the master before proposing a change. The newer document is often the copy that drifted.
- A number in a test scenario is no design decision. Where the requirements are silent, the person's knowledge of the user sets the number.
- A name says who a project belongs to. Even when the person delegates naming, the agent should check the choice with them.
- A rule the agent wrote still slips under load. One question without a link or context cost a full round trip.
- Search the map, the contracts, the decisions and the glossary before asking the person anything. A question the files already answer costs the person's trust as well as their time.
- Verify a claim from an audit or another session against the files before passing it on.
- Describe how two parts relate by mechanism: code, network, data, dependency or contract. A word with several meanings, such as "part of", hides which one is meant.
- Give the workspace a territory. It specifies the contracts between repositories and the checks that compare both sides. Domain knowledge and each repository's implementation belong elsewhere.
- Read the code and the knowledge file before writing a requirement about them. "Comes from" can mean "is stored in" or "is equal to"; say which.
- Check every round of fixes with a fresh agent. A fix often credits a source with more than it says.
- Quote the person's answer in the decision it settles. A project file that paraphrases it cannot outweigh a shared rule.
- Give a new milestone its work items in its first pull request, or the gate has nothing to show.
- One writer per branch. Helpers each take one repository; the lead merges after checking.
- Keep a check's baseline in the repository whose problems it lists, so a fix and its lower count travel in one pull request.
- Run a new check on the check itself first.
- Make approval easy. One page per milestone, one line per requirement, generated from the files so it never goes stale.
- Finish a milestone's checklist in order. Approval of the next milestone comes last, because the open items before it can still change what is approved.
- Updating the lesson log is part of finishing a session. Without a written rule, the agent forgot it.
- The strongest model available, at high effort, made every mistake in this log. The files, the checks and the person's questions are what stopped them repeating.
- Hard-wrapped Markdown read as one run-on sentence on GitHub. The agent wrapped lines by habit; a rule in CLAUDE.md and a one-time reflow of 46 files fixed it.
- Check an audit's findings against the decisions and the owning repository's documents before acting on them. Two of the ten were settled designs read wrongly.
- Two ID series that differ only by a hyphen read as one. Put the owner in the ID: Q-WS-120 and Q-E2-120.
- A child repository's plan drifts into a release of its own. The workspace sets releases for all repositories, and each child plan names the workspace milestone it serves.
- Work under review lives on a branch until it merges. A request to review it links the file on the branch and the pull request; the author looked on `main` and found nothing.
- A repository setting that blocks the agreed way of working is a blocker to report, with the change it needs and why. The agent called PCM-Adapter's review rule the author's choice; under spec-driven work with self-merge (WD-009) it was a change the work needed.
- A milestone list can read well file by file and still leave requirements in no milestone. Count membership with a script.
- Gather work that needs a place only the person can reach into one milestone, so the others can finish without them.
- A request answered in part reads as done. Check each request of the person against what was delivered, word for word.
- Read the data a design document relies on before writing a claim about it.
- A loop that prints check results does not stop a commit. Make the commit depend on the checks' exit code.
- Restore a planted break from a copy. A version-control command that restores a file also discards the edits not yet committed.
- The expert gives input and the agent decides. An answer goes into the goal, scope, constraint, assumption or requirement it changes, with the expert's words as its reason.
- A separate log of the expert's answers turns them into rulings, and an agent executes rulings. Keep each reason with what it shaped.
- A reason shared by many items gets one home of its own, a principle or a constraint, and the items cite it.
- A design choice is the architect's. Ask the expert for what the choice depends on, then decide, and write the options and reasons so the expert can check them and learn.
- A question that offers options asks for a decision. Ask for the knowledge behind it, and state the assumption the work uses until the answer comes.
- A check that needs a file is no reason to keep the file. Change the check with the method, in the same three steps as a contract.
- Count again before quoting another session's number. Its count may have left out a repository.
- Writing about files that are still being written works when the order is agreed, and when each example is checked against the files once they land.
