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

Each correction went into `DECISIONS.md` and `SYSTEM.md`.

**4. Decisions.** The author answered six questions in a few words each: who owns the KPI definitions, where decisions live, the git workflow, the exam, the public site's model, where credentials live. These became DECISIONS W-001 to W-011.

**5. The checks.** The agent wrote two checks and proved each one could fail by planting a break:

- **C1** compared 49 sub-metrics across 6 KPIs. All the limits agreed. 11 names differed. Those became a baseline and an open question.
- **C3** started the real knowledge service and called it with the web app's own client. No differences.

**6. The pull request.** All files and checks went into one pull request for the author's review, because it held new cross-repo decisions.

## Lessons from the log

- The survey was useful because it was wrong in places: each error pointed to a missing document.
- The author's time went into answers and decisions, not into explaining the system again.
- The first check found a real, unknown gap on its first run.
- The repository was renamed during the session. The map, the contracts and the checks absorbed it in minutes, because the name was written in a few known places.
