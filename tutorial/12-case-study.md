# 12. Case study log

What happened while this workspace was set up, in order, mistakes included. It covers four days in November 2026.

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

**The trust question.** Discussing AI-written public content, the author noted that keeping an expert site credible is not a new problem. The discussion that followed became [chapter 11](11-trust-in-ai-written-content.md): separate a wrong source from a wrong rewrite, spend scarce review time on disagreements and on the most-read pages, and build a community that can review.

## Day four: names, and the plan against intent

**Names first.** Early that morning, in short sessions, the author asked for names that explain themselves ([chapter 10](10-names-and-vocabulary.md)):

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

**A question with no context.** The agent asked: "Should isvara.io treat `what-to-set` files as configuration, with no Agent E2 change?" The author could not tell what it meant. It named a file type the author had never needed to know, gave no link, and had already been settled by the decision on the topics. [Chapter 4](04-the-interview.md)'s rule was in the files. The agent broke it while summarising many items at once.

**Many decisions in one conversation.** The session changed the plan seven times in a few hours. Each change became its own pull request, and several touched the same lines of the roadmap, so two of them conflicted. The agent built the later ones on top of the earlier ones. Merging the last pull request merged the whole stack.

**"Part of", and a Level 100 question.** Another session audited the management pack and reported six names for it, adding that the repository name "suggests it is part of PCM, which it is not". The agent relayed that sentence to the author as a contradiction and asked: "is the adapter part of PCM?" The workspace already answered it. Three files recorded the author's earlier answer, and the contract file described the mechanism: the adapter computes the KPIs inside VCF Operations, and PCM reads them through the Suite API. The author's reply: technically, PCM never connects to the adapter; functionally, PCM's live scenario has no data without it. "Part of" had two meanings, and the agent used the word without saying which. The author asked what else the agent might not know. The relation is now written by mechanism in [SYSTEM.md](../SYSTEM.md), and the working rules say: search the files before asking, verify an audit's claim before relaying it, and describe a relation by mechanism.

**The workspace in the wrong territory.** Asked to approve milestone M2, the author pointed out two problems. The first was the approval itself: its requirements were spread over four files, and approving meant reading each one and its numbers. The second was worse. A requirement said the scoring rules were "defined once, in the catalog, with worked examples". The catalog is a list of data rows: one row per metric with five limits. The scoring model is explained in Agent E2's knowledge and implemented in the management pack's code, and nothing reads the other at run time. An earlier session had turned the author's answer "all their logic should come from Agent E2" into a storage mechanism, without reading the code. Two more requirements restated a capacity formula that Agent E2 already held. The fix was a rule about territory: the workspace specifies only where repositories meet, Agent E2 holds the domain knowledge, and each repository specifies its own implementation. A generated review page now lists each milestone's requirements on one page, one line each.

**Asking for approval too early.** With the review page built, the agent asked the author to approve milestone M2. The author asked why it had jumped to M2 while M1 was unfinished. Approving M2 was the last item of M1, and four items above it were still open: requirements to update, isvara.io's requirements to write, the files to check against the new territory rule, and the milestones to renumber. Any of them could still change M2. The agent had read the line it wanted and skipped the checklist around it.

**The lesson log.** At the end the agent reported that nothing was outstanding. The author asked whether this tutorial had been updated with the session's lessons, "or you forget about it, again?" It had not. Updating this log is now a rule for the end of every session in the agent's working rules ([CLAUDE.md](../CLAUDE.md)).

**The cold-read audit, answered.** A fresh session read the five repositories the way a newcomer would and listed the names it could not guess. The author's answers sorted its findings. Two were already settled: WD-032 had decided the management pack's name, and agent-e2's benchmark questions keep a file name and a separate ID on purpose, which agent-e2's documentation says. Others became changes across all five repositories: question IDs that name their repository (Q-WS-, Q-E2-), releases defined only in the workspace, milestones renumbered in the order of work, no hand-written counts, and every child README linking the workspace. The audit also misread one name: `story_m5` holds PCM's demo story M-5, which the audit took for milestone 5.

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
- Make approval easy. One page per milestone, one line per requirement, generated from the files so it never goes stale.
- Finish a milestone's checklist in order. Approval of the next milestone comes last, because the open items before it can still change what is approved.
- Updating the lesson log is part of finishing a session. Without a written rule, the agent forgot it.
- The strongest model available, at high effort, made every mistake in this log. The files, the checks and the person's questions are what stopped them repeating.
- Hard-wrapped Markdown read as one run-on sentence on GitHub. The agent wrapped lines by habit; a rule in CLAUDE.md and a one-time reflow of 46 files fixed it.
- Check an audit's findings against the decisions and the owning repository's documents before acting on them. Two of the ten were settled designs read wrongly.
- Two ID series that differ only by a hyphen read as one. Put the owner in the ID: Q-WS-120 and Q-E2-120.
- A child repository's plan drifts into a release of its own. The workspace sets releases for all repositories, and each child plan names the workspace milestone it serves.
