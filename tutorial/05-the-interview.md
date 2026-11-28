# 5. The interview

## Purpose

A goal such as "connect the web app to the live system" leaves dozens of things open. Which pages? What happens when data is missing? Does the demo data stay? If nobody asks, the agent answers each of these itself while it builds, and you find out which answers you disagree with when you see the result. The interview moves those questions to the start, where an answer costs a few words.

The interview gathers input. It asks the person for what only the person knows: goals, scope, what users expect, field knowledge, constraints, assumptions to confirm, and the reasons behind them. Everything else, the agent decides.

## Four kinds of finding

The agent reads every repository and lists four kinds of finding. The examples are from this project.

| Kind | What it means | Example |
|---|---|---|
| Conflict | Two documents say different things | One document says the web app computes the scores; another says it only reads them |
| Undecided | Something is marked "later", "to check" or left blank | "Release 1.0: placeholder values", while the roadmap asks for live data |
| Unstated assumption | Code or plans rely on something no document states | The demo data has 13 months of history; the lab has a few days |
| Missing requirement | An outcome is wanted but nobody said how to check it | "The answer must match the live system", with no rule for the comparison |

Each finding the agent cannot settle from the files becomes a question. In this project four agents surveyed the four repositories in parallel, since the surveys did not depend on each other, and each returned its list with links to the exact lines that proved each finding. About 80 findings were merged into 61 questions.

## Questions that ask for input

The first rounds in this project asked the author to approve a recommendation. Each question offered options and a recommended answer, and most answers were "Agree". That form had a cost the project noticed late: every "Agree" was recorded as the author's decision, and the agent then executed it as an order ([chapter 2](02-the-method.md)). It also put design choices in front of the person who should have been asked for knowledge.

Three questions from this project show the difference.

- **Input given where a decision was asked.** Q-WS-27 asked when a value counts as stale and recommended 15 minutes. The author answered with a requirement and its reason: "PCM simply regurgitate the adapter. If the data is stale, say no data. No need to wait 15 minutes." The number then became the agent's design: 10 minutes, one collection cycle of the adapter plus a margin of one cycle, so a single late collection does not blank the screen ([chapter 7](07-requirements-and-acceptance.md)).
- **A design put to the expert.** Q-WS-136 offered three designs for isvara.io's guard against instructions hidden in a question, and asked the author to choose. That is a security design, and the agent's to make. The input it depended on was already in the files: the guard sits in isvara.io (the author's answer to Q-WS-47), and model spending stays within US$50 a month. The author's answer asked for the reasoning instead of a choice: "Ok. Document the answers so human readers can learn from it."
- **A question for field knowledge.** Q-WS-137 asks for the key of one metric in VCF Operations, which no document names. It says what the agent will do without an answer: read the lab in milestone M8, and if no such key exists, turn the catalog row into a 5-minute value without "peak" in its name. Field knowledge settles it at once; without it, the work goes on.

## Parts of a good question

Each question in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) has the same parts:

- what the files say now, with links to the lines;
- the input needed, in the person's words, with no term only the agent knows;
- what it blocks, and from which milestone;
- the working assumption the agent uses until the answer comes, and what it will do with each likely answer;
- an empty `Answer:` line.

The working assumption keeps the work moving, and it shows the person what will be built if they say nothing. It is recorded as an assumption ([chapter 6](06-constraints-assumptions-risks-dependencies.md)), and the answer confirms it or replaces it.

Each part matters. In this project the agent once asked whether isvara.io should "treat `what-to-set` files as configuration". The author had no idea what that meant: no link, no context, and a file type only the agent knew. A question the person cannot understand costs a full round trip.

The person answers by editing the file on GitHub, in their own time. Answers given in chat scroll away, and the next session cannot see them.

## Questions the agent answers itself

An interview full of questions the agent could answer itself wastes the person's time and their trust. In this project the agent asked where "availability" belongs among operations disciplines, which any practitioner knows. Anything that can be found in the documents, the code or general knowledge of the field, the agent decides and states, and the person can still overrule it. Design questions belong here too: security, performance, scalability and maintainability are the architect's work ([chapter 8](08-design.md)).

## Answers and where they go

An answer changes the specification directly. It goes into the goal, scope line, constraint, assumption or requirement it affects, with the person's words as the reason. Nothing else needs to record it.

Expect more than one round. Writing the requirements from the first round's answers raised 66 new questions in this project, smaller and more precise than the first: names, exact numbers, limits. Each round is kept as a record, with the author's answers exactly as written, in [spec/author-input](../spec/author-input/interview-round-1.md), and requirements cite them by question number. When the person asks for an explanation to be kept, as the author did for the injection guard, the record keeps the question's whole text.

## Exercise

Ask your agent to survey one of your repositories for the four kinds of finding, with a link to the line for each. Sort its questions into three piles: input only you can give, design the agent should decide, and facts it could have looked up. Only the first pile should reach you.
