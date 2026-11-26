# Building software with an AI agent: a spec-driven approach

This tutorial shows how to build and maintain a system of several connected applications when an AI coding agent writes most of the code. It is based on a real project: four GitHub repositories that together make one product, built by one person working with Claude over several months. Every file the tutorial mentions is in this repository, so you can read the real thing alongside the explanation.

## Who it is for

- Builders who already use an AI coding agent for small tasks and want it to carry larger, longer work.
- Domain experts who own the requirements but are not full-time developers.
- Teachers looking for material for a course or workshop. The [teaching guide](teaching-guide.md) has a session plan.

You do not need to know VMware. The project's subject matter is only the example.

## Two ways to work with an AI agent

### Iterative prompting

This is how most people start, and how this project was built for its first few months. You describe what you want in a chat. The agent does it. You look at the result and ask for the next change. Each conversation is short and covers one task. What the system is, and why it is the way it is, lives in your head and in the code. At the start of each conversation the agent works it out again by reading the code.

### Spec-driven development

Here you write down what the system is and what it must do before you ask the agent to build it, and you keep those notes as files in the repository. In this project the files are:

- a short description of the system and what is in scope now;
- the interfaces between the parts, and which part owns each shared fact;
- the decisions already made, with their reasons;
- requirements written so that each one can be tested, each with its test scenarios;
- the questions still open, waiting for the person to answer.

The agent reads these files at the start of every session and builds against them. Scripts check automatically that the parts still agree with each other. When the agent meets something the files do not cover, it asks, and the answer goes into the files.

### How they compare

| | Iterative prompting | Spec-driven development |
|---|---|---|
| Getting started | Immediate | Days of writing, and of answering the agent's questions |
| Each change | Small and fast | Slower; the spec may need updating first |
| Where knowledge about the system lives | In your head, and scattered across old chats | In files that every session reads |
| A gap in your instructions | The agent fills it with a plausible guess, usually without saying so | The agent turns it into a question for you |
| Interfaces between parts | Checked only if someone remembers to | Checked by scripts on every change |
| Knowing that work is finished | The agent says it is | Its test scenarios pass |
| Changing direction | Easy: ask for something else | The spec changes first, which costs time but leaves a record |
| Typical failure | Drift: copies of the same fact diverge, and old features break quietly | Specs go stale or grow too detailed, and you spend time answering questions |
| Suits | Prototypes, one-off scripts, small self-contained work, exploring an idea | Several connected parts, a system that must last, work spread over many sessions or many people |

### When to use which

The two are not exclusive. Prototyping by prompting is a good way to find out what you want. The trouble starts when the prototype becomes the product and the number of parts grows, because every conversation then has to rediscover what the others decided. In this project that point came when four repositories began to depend on each other: a threshold changed in one place and not in another, and a test passed while the feature it tested was broken in the next repository.

Spec-driven development has real costs, and the tutorial does not hide them:

- **It costs the person time.** In this project the first round of questions had 61 items and the second 66. Most could be answered with "Agree", but someone has to read them.
- **A wrong spec is built faithfully.** The agent will implement a mistaken requirement as carefully as a correct one. The spec needs the same scrutiny as code.
- **Specs need upkeep.** A spec that no longer matches the system is worse than none, so the checks and the habit of writing corrections back matter as much as the first draft.
- **The agent slips back.** Even after writing the method down, the agent in this project twice went back to building first and asking afterwards. [Chapter 11](11-case-study.md) shows both times. The person has to hold the line.

## Chapters

| Chapter | What it covers | Time |
|---|---|---|
| [1. Why small chats fail](01-why-small-chats-fail.md) | What goes wrong when a growing system is built one prompt at a time | 10 min |
| [2. The method](02-the-method.md) | The seven steps, and how they feed each other | 10 min |
| [3. The map](03-map.md) | Describing what exists today, and what is in scope | 15 min |
| [4. The interview](04-the-interview.md) | Getting every open question onto the table before building | 15 min |
| [5. Seams and owners](05-seams-and-owners.md) | Where the parts meet, and which copy of a shared fact is the real one | 20 min |
| [6. Requirements and tests](06-requirements-and-tests.md) | Writing what "done" means so a script or a person can check it | 20 min |
| [7. Checks](07-checks.md) | Scripts that prove the parts still agree | 20 min |
| [8. Slices and sessions](08-slices-and-sessions.md) | The order of work, and how each working session runs | 15 min |
| [9. Working with the agent](09-working-with-the-agent.md) | Who decides what; the agent as co-architect; models and effort | 20 min |
| [10. Trust in AI-written content](10-trust-in-ai-written-content.md) | Keeping published material credible when an AI writes it | 15 min |
| [11. Case study log](11-case-study.md) | What actually happened in this project, mistakes included | 20 min |

The [templates](templates) folder has empty versions of each file, to start your own project.

## The files in this repository

Each is a working example of what the method produces:

| File | What it is | Chapter |
|---|---|---|
| [SYSTEM.md](../SYSTEM.md) and [spec/intent.md](../spec/intent.md) | The map, and why each part exists | 3 |
| [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) and [spec/interview-round-1.md](../spec/interview-round-1.md) | The interview: open questions, and the first round with the author's answers | 4 |
| [CONTRACTS.md](../CONTRACTS.md) and [DECISIONS.md](../DECISIONS.md) | The interfaces between repositories, and the decisions that bind them | 5 |
| [spec/requirements](../spec/requirements) | Requirements with test scenarios | 6 |
| [checks](../checks) and [tools](../tools) | The scripts that check contracts, requirements and documents | 7 |
| [ROADMAP.md](../ROADMAP.md) | The milestones and their order | 8 |
| [CLAUDE.md](../CLAUDE.md) | How the agent is told to work | 9 |
