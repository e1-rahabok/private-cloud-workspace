# 11. Case study log

What happened while this workspace was set up, in order, mistakes included. It covers four days in November 2026.

## The system

Four repositories make one product:

- **Agent E2**, a knowledge service that answers like a VMware performance and capacity expert. It has no user interface.
- **PCM-Adapter**, a management pack that computes performance and capacity scores inside VMware's monitoring product.
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

**The trust question.** Discussing AI-written public content, the author noted that keeping an expert site credible is not a new problem. The discussion that followed became [chapter 10](10-trust-in-ai-written-content.md): separate a wrong source from a wrong rewrite, spend scarce review time on disagreements and on the most-read pages, and build a community that can review.

## Day four: the plan against the person's intent

**The plan had grown.** The session opened with the author's own summary of release 1.0: rebuild isvara.io, add the live demo to PCM, and leave Agent E2 and the management pack nearly untouched. The agent compared it with the roadmap. The files said otherwise: 19 requirements for Agent E2 and 24 for the management pack, in three milestones that the live demo and the site depended on. Each requirement had a source. Together they made a release larger than the author meant, and nobody had noticed. The author then went through the plan item by item.

**Purpose questions shrink a plan.** "What is the grader for? The quiz is multiple choice." The grader scored Agent E2's free-text answers, which the quiz never uses. Once its purpose was stated, the author kept it at 15 questions instead of 40 and moved the rest to the plan after 1.0. The same kind of question cut the management pack's data states to one correctness fix, and moved a lab build, value management and three new kinds of knowledge to after 1.0. Each deferral became a decision with a line under "After release 1.0", so nothing was lost.

**A number taken from a test.** Explaining the progress display, the agent said the caller checks every 2 seconds. The author asked whether that was too often: a VMware administrator knows this is no general chat and does not mind 10 seconds. The 2 seconds came from a test scenario. No requirement set the interval at all, and that gap was the real finding. The person's knowledge of the user set the number.

**The copy that drifted.** The new site plan listed the IT management topics as availability, performance, capacity, configuration and security. Agent E2's tag listed availability, performance, security, capacity and value. The agent proposed a new "configuration" tag in Agent E2 to match the plan. The author's answer: Agent E2 is correct; it is what the framework documents. The newer design document had drifted from the master. The agent should have read the framework before proposing to change it.

**Names carry identity.** In an earlier round the author had let the agent decide the management pack's new name and key prefix, and the agent chose "PCM". The author reversed it: the pack is a vCommunity project of vExperts and VMUG members, and its name shows a grassroots effort. In the same exchange the agent suggested renaming the book to match the software. The author explained the difference. The book, Private Cloud Management, is the discipline. Private Cloud Manager and isvara.io are two applications built on it, for the same audience and different uses.

**A question with no context.** The agent asked: "Should isvara.io treat `what-to-set` files as configuration, with no Agent E2 change?" The author could not tell what it meant. It named a file type the author had never needed to know, gave no link, and had already been settled by the decision on the topics. [Chapter 4](04-the-interview.md)'s rule was in the files. The agent broke it while summarising many items at once.

**Many decisions in one conversation.** The session changed the plan seven times in a few hours. Each change became its own pull request, and several touched the same lines of the roadmap, so two of them conflicted. The agent built the later ones on top of the earlier ones. Merging the last pull request merged the whole stack.

**The lesson log.** At the end the agent reported that nothing was outstanding. The author asked whether this tutorial had been updated with the session's lessons, "or you forget about it, again?" It had not. Updating this log is now a rule for the end of every session in the agent's working rules ([CLAUDE.md](../CLAUDE.md)).

## Lessons

- The agent's first survey was useful precisely because it was wrong in places. Each error pointed to a missing document.
- The author's time went into answers and decisions instead of explaining the system again.
- A check written in an afternoon found a real gap on its first run.
- An agent drifts back to building first even after writing down the method. A short question from the person, such as "is the interview done?", brings it back.
- A convention the agent has read about is not a convention it follows. Only a script makes it hold.
- Most answers can be one word when each question carries a recommendation.
- A specification raises its own questions. Expect a second round.
- The agent is most useful when it argues. The best design idea in this log came from the author, in reply to the agent's critique of the author's first idea.
- Compare the plan with the person's intent at the start of each release. Requirements with good sources can still add up to a release nobody asked for.
- Ask what each planned item is for. An item whose purpose takes more than a sentence to explain is a candidate for later.
- A deferral is a decision, with its own line in the plan after the release.
- When two documents disagree, find the master before proposing a change. The newer document is often the copy that drifted.
- A number in a test scenario is no design decision. Where the requirements are silent, the person's knowledge of the user sets the number.
- A name says who a project belongs to. Even when the person delegates naming, the agent should check the choice with them.
- A rule the agent wrote still slips under load. One question without a link or context cost a full round trip.
- Updating the lesson log is part of finishing a session. Without a written rule, the agent forgot it.
- The strongest model available, at high effort, made every mistake in this log. The files, the checks and the person's questions are what stopped them repeating.
