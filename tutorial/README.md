# Building software with AI: a method and a case study

How to build a system of several connected applications when an AI agent writes the code, and how to keep it correct as it grows. The method is shown on a real case, this workspace: four repositories that form one product, built by one person with Claude.

## Who it is for

- Builders who already use an AI coding agent on small tasks and want it to carry larger, longer work.
- Domain experts who are not full-time developers but own the requirements.
- Teachers who want material for a course or a workshop: see the [teaching guide](teaching-guide.md).

No knowledge of VMware is needed. The case study's domain is only the example.

## The idea in one paragraph

An AI agent implements what it is told and invents the rest. Over thousands of small conversations, what it invents drifts, and nobody notices until something breaks. The fix is not longer prompts. It is a small set of files the agent reads at the start of every session: what the system is, where its parts meet, who owns each fact, what "done" means for each piece of work, and code that checks the meeting points automatically. The human decides; the agent builds and checks.

## Reading order

| Chapter | Question it answers | Time |
|---|---|---|
| [1. Why small chats fail](01-why-small-chats-fail.md) | What goes wrong without a method? | 10 min |
| [2. The method](02-the-method.md) | What are the six steps? | 10 min |
| [3. The map](03-map.md) | What exists today, and what is in scope? | 15 min |
| [4. Seams and owners](04-seams-and-owners.md) | Where do the parts meet, and which copy of a fact wins? | 20 min |
| [5. Definition of done](05-definition-of-done.md) | How does the agent know it has finished? | 15 min |
| [6. Checks](06-checks.md) | How are the seams verified without a person? | 20 min |
| [7. Slices and sessions](07-slices-and-sessions.md) | In what order, and how is each session run? | 15 min |
| [8. Working with the AI](08-working-with-ai.md) | Who decides what? Which model, which effort? | 15 min |
| [9. Case study log](09-case-study.md) | What actually happened, including the mistakes? | 15 min |

[Templates](templates) holds empty versions of every file, to start your own project.

## The files the method produces

In the root of this repository, each one a working example:

| File | Step |
|---|---|
| [SYSTEM.md](../SYSTEM.md) | The map |
| [CONTRACTS.md](../CONTRACTS.md) | The seams |
| [DECISIONS.md](../DECISIONS.md) | The owners and other decisions |
| [ROADMAP.md](../ROADMAP.md) | Slices with definitions of done |
| [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) | What only the human can answer |
| [CLAUDE.md](../CLAUDE.md) | How the agent works |
| [checks/](../checks) | The checks |
