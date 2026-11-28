# 4. The interview

## Purpose

A goal such as "connect the web app to the live system" leaves dozens of things open. Which pages? What happens when data is missing? Does the demo data stay? If nobody asks, the agent answers each of these itself while it builds, and you find out which answers you disagree with when you see the result. The interview moves those questions to the start, where a one-word answer costs nothing.

## Four kinds of finding

The agent reads every repository and lists four kinds of finding. The examples are from this project.

| Kind | What it means | Example |
|---|---|---|
| Conflict | Two documents say different things | One document says the web app computes the scores; another says it only reads them |
| Undecided | Something is marked "later", "to check" or left blank | "Release 1.0: placeholder values", while the roadmap asks for live data |
| Unstated assumption | Code or plans rely on something no document decides | The demo data has 13 months of history; the lab has a few days |
| Missing requirement | An outcome is wanted but nobody said how to check it | "The answer must match the live system", with no rule for the comparison |

Each finding becomes a question. In this project four agents surveyed the four repositories in parallel, since the surveys did not depend on each other, and each returned its list with links to the exact lines that proved each finding. About 80 findings were merged into 61 questions.

## Parts of a good question

Each question in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) has the same parts:

- what the files say now, with links to the lines;
- why it matters, or what it blocks;
- a recommended answer, with the reason;
- an empty `Answer:` line.

The recommendation does most of the work. The person reads it and writes "Agree", or writes their own answer where the recommendation is wrong. In this project most answers were one word, and the rest were the corrections that mattered: the live demo is a separate demo, not a switch; the management pack may change everything; the public site is rebuilt from scratch.

The same parts apply to a question asked in chat. In this project the agent once asked whether isvara.io should "treat `what-to-set` files as configuration". The author had no idea what that meant: no link, no context, and a file type only the agent knew. A question the person cannot understand costs a full round trip.

The person answers by editing the file on GitHub, in their own time. Answers given in chat scroll away, and the next session cannot see them.

## Questions the agent answers itself

An interview full of questions the agent could answer itself wastes the person's time and their trust. In this project the agent asked where "availability" belongs among operations disciplines, which any practitioner knows. Questions are for judgement, field experience, scope and taste. Anything that can be found in the documents, the code or general knowledge of the field, the agent decides and states, and the person can still overrule it.

## Rounds

Expect more than one round. Writing the requirements from the first round's answers raised 66 new questions in this project, smaller and more precise than the first: names, exact numbers, limits. Keep each round as a record. Here the first round, with the author's answers exactly as written, is kept in [spec/interview-round-1.md](../spec/author-input/interview-round-1.md), and requirements cite it by question number. An answered question usually leaves only its answer and its result in the record. When the person asks for the explanation to be kept, as the author did for the question on the injection guard ("Document the answers so human readers can learn from it"), the record keeps the question's whole text, and a requirement plans the page for readers.

## Exercise

Ask your agent to survey one of your repositories for the four kinds of finding, with a link to the line for each. How many of its questions could it have answered itself?
