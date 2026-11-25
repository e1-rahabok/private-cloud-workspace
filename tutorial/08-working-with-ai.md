# 8. Working with the AI

## Who decides what

| The human | The agent |
|---|---|
| Goals and scope | Survey of the code and documents |
| Which copy of a fact is the master | Finding where copies disagree |
| Trade-offs that need field experience | Drafting the specification and definitions of done |
| Approving contract changes and cross-repo decisions | Building, testing, writing checks |
| Answering OPEN-QUESTIONS | Asking, with a recommendation, instead of guessing |

The agent should challenge the human too. In this workspace, one repository's rules ask the agent to act as a co-designer and to say when a request conflicts with an earlier decision. A good question from the agent, such as "your documents disagree on who owns the KPI definitions", is worth more than a fast answer built on a guess.

## Asking good questions

When the agent asks, each question should:

- stand on its own, naming the files and the conflict;
- give a recommendation and the reason;
- say what is blocked until it is answered.

The human then answers in a word or two. See [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) for the format.

## Correcting the agent

Corrections are the most valuable input in the whole process. Put each one into a file. In this case study, the author corrected the agent's framing as well as its facts: it had treated a benchmark as a contest to win, while the author cared only that the product works. Both kinds of correction go into the files so the next session starts from them.

## Choosing a model and effort

Use the strongest model and a high reasoning effort for the steps where a mistake spreads:

- surveying the system and finding conflicts;
- writing the map, contracts and definitions of done;
- reviewing finished work against the specification.

A cheaper, faster model is fine for work that is fully specified: applying agreed edits, filling a table, running a known procedure.

Compare models on your own work rather than on claims. Give two models the same slice and specification, and count the rework each needs, using your checks and a fresh review. Repositories of a few hundred to a few thousand files, like the four here, fit comfortably within a strong model's reach when the method gives it the right files to read.

## A fresh reviewer

Review finished work in a new session that sees only the specification and the change. It is not anchored on the builder's reasoning, so it catches different mistakes.

## Secrets

The agent never sees a password. In this workspace, credentials are encrypted files that only the author's Windows account can decrypt, created by the author with a command that prompts for the password. Scripts load them; nothing prints, logs or commits them. On a Linux server they live in a root-only environment file.
