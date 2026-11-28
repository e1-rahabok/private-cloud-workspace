# Spec-driven development with an AI agent

If you're not familiar with SDD, read this https://github.com/github/spec-kit/blob/main/README.md#spec-driven-development. This tutorial shows how to build and maintain a system of several connected applications when an AI coding agent writes most of the code. It is based on a real project: four GitHub repositories that together make one product, built by one person working with Claude over several months. Every file the tutorial mentions is in this repository, so you can read the real thing alongside the explanation.

## Readers

- VMware administrators and architects who use an AI agent for small tasks, such as a PowerCLI script, and want it to carry larger work. No programming background is assumed.
- Other domain experts who own the requirements but are not full-time developers.
- Teachers and presenters. The [teaching guide](teaching-guide.md) has a plan for a workshop or a series of video calls.

The examples come from a VMware project. If you know VMware, the table below links each step to work you already do. If you don't, skip the table; the method does not depend on it.

## The method in VMware terms

| In spec-driven development | What a VMware administrator already does |
|---|---|
| The map | The current-state section of a design document |
| Goals and scope | Business requirements, scope, and what is out of scope |
| The interview | A design workshop: the customer gives requirements and confirms assumptions |
| Constraints, assumptions, risks, dependencies | The same four sections of a conceptual design |
| Requirements with acceptance criteria | Requirements the customer signs off, each with how it is accepted |
| Design choices | Design decisions, each with its justification and impact |
| Quality attributes | Design qualities: availability, manageability, performance, recoverability, security |
| Seams and owners | Interfaces between teams: who owns DNS, storage, the vCenter |
| Test plan and traceability | The test plan signed off before handover, mapped to the requirements |
| Checks | A compliance check against a host profile, run on a schedule |
| Known gaps | Accepted exceptions in a compliance report, each with an owner |
| Slices | A pilot cluster before the full rollout |
| The agent's working rules | Runbooks and procedures for a new team member |
| Stop conditions | Change rules: stop and escalate when the plan does not cover it |
| The case log | Post-incident reviews, written so the next team learns |

The roles match too. The customer brings the requirements, the constraints and the knowledge of the business; the architect writes the design and justifies each decision. In this method the person is the customer and the domain expert, and the agent is the architect.

The difference is upkeep. A design document is written once and goes stale. Here the agent reads the files at the start of every session, and scripts check them on every change, so they stay true.

## Two ways to work with an AI agent

### Iterative prompting

This is how most people start, and how this project was built for its first few months. You describe what you want in a chat. The agent does it. You look at the result and ask for the next change. Each conversation is short and covers one task. What the system is, and why it is the way it is, lives in your head and in the code. At the start of each conversation the agent works it out again by reading the code.

### Spec-driven development

Here you write down what the system is and what it must do before you ask the agent to build it, and you keep those notes as files in the repository. In this project the files are:

- a brief: the goals, the scope and the principles, and the constraints, assumptions, risks and dependencies;
- requirements written so that each one can be tested, each with its reason, its acceptance criteria and its test scenarios;
- a design: the parts, the interfaces between them, which part owns each shared fact, and each design choice with its reasons and the options it rejected;
- a test plan, with a chain of IDs from each goal to the test that proves it;
- the questions still open, each asking the person for input.

The person supplies the input: goals, scope, users, domain knowledge, constraints and reasons. The agent decides the rest, writes each decision where it takes effect, and shows its reasoning. It reads these files at the start of every session and builds against them. Scripts check automatically that the parts still agree with each other. When the agent meets something the files do not cover, it asks for the input it lacks, and the answer goes into the files.

### Comparison

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

### Choosing between them

The two are not exclusive. Prototyping by prompting is a good way to find out what you want. The trouble starts when the prototype becomes the product and the number of parts grows, because every conversation then has to rediscover what the others decided. In this project that point came when four repositories began to depend on each other: a threshold changed in one place and not in another, and a test passed while the feature it tested was broken in the next repository.

Spec-driven development has real costs, and the tutorial does not hide them:

- **It costs the person time.** In this project the first round of questions had 61 items and the second 66. Most could be answered with "Agree", but someone has to read them.
- **A wrong spec is built faithfully.** The agent will implement a mistaken requirement as carefully as a correct one. The spec needs the same scrutiny as code.
- **Specs need upkeep.** A spec that no longer matches the system is worse than none, so the checks and the habit of writing corrections back matter as much as the first draft.
- **The agent slips back.** Even after writing the method down, the agent in this project twice went back to building first and asking afterwards, and for weeks it treated the person's answers as decisions to execute. [Chapter 16](16-case-study.md) shows each time. The person has to hold the line.

## Chapters

| Chapter | What it covers | Time |
|---|---|---|
| [1. The limits of small chats](01-why-small-chats-fail.md) | What goes wrong when a growing system is built one prompt at a time | 10 min |
| [2. The method](02-the-method.md) | The nine steps, who leads each, and one home for each reason | 15 min |
| [3. The map](03-map.md) | Describing what exists today | 15 min |
| [4. Goals and scope](04-goals-and-scope.md) | What the product must achieve, for whom, and what is out | 15 min |
| [5. The interview](05-the-interview.md) | Asking the person for input before building | 15 min |
| [6. Constraints, assumptions, risks and dependencies](06-constraints-assumptions-risks-dependencies.md) | The conditions the work happens under, each handled its own way | 20 min |
| [7. Requirements and acceptance criteria](07-requirements-and-acceptance.md) | Writing what "done" means, with its reason, so it can be checked | 20 min |
| [8. Design](08-design.md) | How the parts meet the requirements, and what a visitor sees | 30 min |
| [9. Seams and owners](09-seams-and-owners.md) | Where the parts meet, and which copy of a shared fact is the real one | 20 min |
| [10. Test plan and traceability](10-test-plan-and-traceability.md) | Levels, environments, journeys, lab run order, oracle, traceability | 20 min |
| [11. Checks](11-checks.md) | Scripts that prove the parts still agree | 20 min |
| [12. Slices and sessions](12-slices-and-sessions.md) | The order of work, and how each working session runs | 15 min |
| [13. Working with the agent](13-working-with-the-agent.md) | Input and decisions; the agent as architect, then implementer; models and effort | 20 min |
| [14. Names and vocabulary](14-names-and-vocabulary.md) | Names, IDs and folders the agent can guess | 15 min |
| [15. Trust in AI-written content](15-trust-in-ai-written-content.md) | Keeping published material credible when an AI writes it | 15 min |
| [16. Case study log](16-case-study.md) | What actually happened in this project, mistakes included | 30 min |
| [17. Your first project](17-your-first-project.md) | A week-long plan to try the method on your own work | 10 min |

The [templates](templates) folder has empty versions of each file, to start your own project.

## The files in this repository

Each is a working example of what the method produces:

| File | What it is | Chapter |
|---|---|---|
| [spec/README.md](../spec/README.md) | The specification's own map: its files, IDs and who writes what | 2 |
| [spec/design/system.md](../spec/design/system.md) | The system's parts, contracts, quality attributes and design choices | 3, 8, 9 |
| [spec/brief.md](../spec/brief.md) | Goals, scope, principles, constraints, assumptions, risks, dependencies | 4, 6 |
| [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) and [spec/author-input](../spec/author-input/interview-round-1.md) | The input still needed, and the interview rounds with the author's answers | 5 |
| [spec/requirements](../spec/requirements) | Requirements with acceptance criteria and test scenarios | 7 |
| [spec/test-plan.md](../spec/test-plan.md) | The test plan and the traceability chain | 10 |
| [checks](../checks) and [tools](../tools) | The scripts that check contracts, requirements and documents | 11 |
| [ROADMAP.md](../ROADMAP.md) | The milestones and their order | 12 |
| [CLAUDE.md](../CLAUDE.md) | How the agent is told to work | 13 |
| [spec/glossary.md](../spec/glossary.md) | Every ID and term, with its meaning | 14 |
| [DECISIONS.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/8677e71/DECISIONS.md), as it was | The decision log the specification replaced | 2 |
