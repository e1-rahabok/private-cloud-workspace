# 11. Case study log

What happened while this workspace was set up, in order, mistakes included. It covers three days in November 2026.

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

## What the log teaches

- The agent's first survey was useful precisely because it was wrong in places. Each error pointed to a missing document.
- The author's time went into answers and decisions instead of explaining the system again.
- A check written in an afternoon found a real gap on its first run.
- An agent drifts back to building first even after writing down the method. A short question from the person, such as "is the interview done?", brings it back.
- A convention the agent has read about is not a convention it follows. Only a script makes it hold.
- Most answers can be one word when each question carries a recommendation.
- A specification raises its own questions. Expect a second round.
- The agent is most useful when it argues. The best design idea in this log came from the author, in reply to the agent's critique of the author's first idea.
- The strongest model available, at high effort, made every mistake in this log. The files, the checks and the person's questions are what stopped them repeating.
