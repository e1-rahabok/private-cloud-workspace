# 9. Case study log

What happened in the session that set up this workspace, in order, including the mistakes. Dates are 2026.

## The system

Four repositories, one product:

- **Agent E2**: a knowledge service that answers like a VMware performance and capacity expert. No user interface.
- **PCM-Adapter**: a plug-in for VMware's monitoring product that computes performance and capacity scores.
- **PCM**: a web app for operations teams that shows those scores and asks Agent E2 to explain them.
- **isvara.io**: a public learning site that will also use Agent E2.

All built with AI over several months, through thousands of small conversations.

## The session, step by step

**1. The question.** The author asked whether a long, complex chain of tasks was a reasonable thing to give an AI, given that the high-level goals felt too abstract to be instructions. The answer: yes, if the goals are paired with checkable definitions of done and the seams are checked by code.

**2. The survey.** The agent read the four repositories. It found that two were already well specified (one with over a hundred numbered decisions), and that the gaps were between the repositories: an almost empty parent repository, no list of contracts, decisions in three places, and conflicting rules.

**3. Corrections from the author.** The agent's survey got four things wrong:

| The agent said | The truth | Why it was wrong |
|---|---|---|
| The knowledge service's cloud model conflicts with its "local model" mission | The cloud model is for the demo; local is a later stage | The parent repository did not say so |
| The adapter is a separate product | It is part of PCM | One repository's decision log said so; the parent did not |
| PCM moves from demo data to live data | It keeps both | Never written down |
| Publishing exam questions risks a benchmark contest | The author does not care about contests | The agent assumed a goal the author did not have |

Each correction went into [`DECISIONS.md`](../DECISIONS.md) and [`SYSTEM.md`](../SYSTEM.md).

**4. Decisions.** The author answered six questions in a few words each: who owns the KPI definitions, where decisions live, the git workflow, the exam, the public site's model, where credentials live. These became DECISIONS W-001 to W-011.

**5. The checks.** The agent wrote two checks and proved each one could fail by planting a break:

- **C1** compared 49 sub-metrics across 6 KPIs. All the limits agreed. 11 names differed. Those became a baseline and an open question.
- **C3** started the real knowledge service and called it with the web app's own client. No differences.

**6. The pull request.** All files and checks went into one pull request for the author's review, because it held new cross-repo decisions.

**7. The agent skipped its own advice.** With the files merged, the agent proposed starting the first build milestone. The author stopped it with three questions: is the interview done? Are the requirements written, each one testable? Are the stop conditions in place? The honest answers were: no, no, and partly. Six questions answered in chat is not an interview; the milestones were bullet points, not requirements with test scenarios. The agent had fallen back into the pattern the method exists to replace: building, then asking the author to react.

**8. The interview, done properly.** Four agents surveyed the four repositories in parallel, each listing every conflict, undecided item, unstated assumption and missing requirement, with links to the lines that prove it. About 80 findings were merged into 61 questions, grouped by area, each with a recommendation and an empty `Answer:` line that the author fills in on GitHub. The roadmap gained a milestone with no code in it: interview and specification first, then build.

**9. The author's conventions were missed at first.** The author's other repositories already had two conventions the new files ignored: every file reference is a clickable link, and every diagram is an SVG with its text generated underneath for machines. The agent had read those repositories and still used plain paths and text drawings. Both now have a tool and a check, so they cannot be missed again.

**10. The answers, and the whole specification.** The author answered nearly all 61 questions on GitHub in one evening, often in a few words, and corrected several assumptions: the live demo is a separate demo of one role, the management pack may change everything, the public site is rebuilt from scratch. The agent then moved the answers into decisions and an intent page, and four agents, the same ones that ran the surveys and still held their context, drafted the requirements of their repository in parallel: 105 requirements with 176 test scenarios, each citing the answer it came from. A check confirms every requirement has a source and a test. Writing the requirements raised 66 new questions, mostly naming and exact numbers, which became round 2.

**11. A self-inflicted loss.** While gathering the round-two questions from six new files, a script rewrote the files before it had saved what it collected, and the save failed. The files were new and not yet committed, so git could not restore them; the agent rebuilt the questions from what it had read earlier. Commit drafts early: an uncommitted file has no undo.

## Lessons from the log

- The survey was useful because it was wrong in places: each error pointed to a missing document.
- The author's time went into answers and decisions, not into explaining the system again.
- The first check found a real, unknown gap on its first run.
- The repository was renamed during the session. The map, the contracts and the checks absorbed it in minutes, because the name was written in a few known places.
- An agent drifts back to "build, then ask" even after writing the method down. The human's best tool is a short question: "is the interview done?"
- A convention the agent "knows" is not a convention it follows. Only a check makes it hold.
- One honest survey found about 80 open points across four repositories that had been built through thousands of conversations. Each one is a guess the next build would have made.
- Answers in a few words are enough when each question carries a recommendation: most answers were "Agree", and the rest were exactly the corrections that mattered.
- A specification raises its own questions. Expect a second round, smaller and more precise than the first.
