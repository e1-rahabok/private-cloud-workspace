# 2. The method

The method has seven steps. The first four are done before any building starts, and their files are kept up to date afterwards. The last three repeat for every piece of work.

| Step | Question it answers | Files | Chapter |
|---|---|---|---|
| 1. Map | What exists today, and what is in scope? | [SYSTEM.md](../SYSTEM.md), [spec/intent.md](../spec/intent.md) | [3](03-map.md) |
| 2. Interview | What is still undecided, unclear or contradictory? | [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) | [4](04-the-interview.md) |
| 3. Seams and owners | Where do the parts meet, and which copy of each shared fact is the real one? | [CONTRACTS.md](../CONTRACTS.md), [DECISIONS.md](../DECISIONS.md) | [5](05-seams-and-owners.md) |
| 4. Requirements | What must each part do, and how will we know it does? | [spec/requirements](../spec/requirements) | [6](06-requirements-and-tests.md) |
| 5. Checks | Do the parts still agree, after every change? | [checks](../checks), [tools](../tools) | [7](07-checks.md) |
| 6. Slices | In what order do we build? | [ROADMAP.md](../ROADMAP.md) | [8](08-slices-and-sessions.md) |
| 7. Run | How does each working session go? | [CLAUDE.md](../CLAUDE.md) | [8](08-slices-and-sessions.md), [9](09-working-with-the-agent.md) |

![The seven steps in a row, from Map to Run, with an arrow from Run back to Map for corrections, answers and new decisions](../images/method.svg)

<details>
<summary>Text of the diagram, for readers that cannot see it</summary>

Colour key: blue = Before building, then kept current; green = Repeated for every slice.

Boxes, nested as drawn:
- n1 **1. Map** (Before building, then kept current): SYSTEM.md intent.md
- n2 **2. Interview** (Before building, then kept current): OPEN-QUESTIONS
- n3 **3. Seams, owners** (Before building, then kept current): CONTRACTS.md DECISIONS.md
- n4 **4. Requirements** (Before building, then kept current): requirements/
- n5 **5. Checks** (Repeated for every slice): checks/, tools/
- n6 **6. Slices** (Repeated for every slice): ROADMAP.md
- n7 **7. Run** (Repeated for every slice): CLAUDE.md

Arrows (from, to, label):
- n1 1. Map --> n2 2. Interview
- n2 2. Interview --> n3 3. Seams, owners
- n3 3. Seams, owners --> n4 4. Requirements
- n4 4. Requirements --> n5 5. Checks
- n5 5. Checks --> n6 6. Slices
- n6 6. Slices --> n7 7. Run
- n7 7. Run --> n1 1. Map: Corrections, answers and new decisions go back into the files

Arrows: `-->` solid, `..>` dashed.

</details>

## How the steps feed each other

Building a slice always teaches something: an assumption on the map that was wrong, a meeting point nobody listed, a question only the person can answer. That goes back into the files before the next slice starts, so the files get more accurate over time instead of falling behind the code.

## The ideas behind the steps

The specification is what the people maintain. The code is generated from it and can be generated again. One of the repositories in this project says so in its own decisions: AI writes all of its code, and people maintain the specification.

Anything that has to outlast a conversation goes into a file in the repository. A conversation is a good place to think something through, but the next session cannot see it.

When a fact appears in more than one place, one copy is the master and the others are generated from it or checked against it.

Every place where two parts depend on each other gets a script that fails when they stop agreeing.

The person makes the decisions that need judgement, field experience or a change of scope. The agent does the rest, and asks when the files do not decide something. Chapter 9 adds an important refinement: the agent should also think and push back, and should not ask the person what it could work out itself.

Work is built in thin slices, each going end to end across every part it touches, starting with the slice that has the most unknowns.

## How long it takes

In this project the first version of the files and two working checks took one long session. The interview and the full set of requirements took another two days, most of it the agent's work, with the author answering questions in the evenings. That is small next to the time the small chats were costing, and the files save that time again at the start of every later session.
