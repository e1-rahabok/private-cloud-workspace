# 3. The map

## The idea

Before any work, write down what the system is: its parts, where each one runs, what talks to what, and which parts of the plan are in scope now. One page. It is `SYSTEM.md` in this repository.

## Current state and target state

The most useful thing a map does is keep **what is** apart from **what will be**. Documents that mix them confuse the agent: it reads "the model runs locally", finds code that calls a cloud model, and either "fixes" the code or stops trusting the document.

In this workspace the plan has two futures:

- **Stage 1 (now):** the product is a demo in a lab. The knowledge service calls a cloud model.
- **Stage 2 (later):** a customer installs it on their own hardware with a local model.

Several documents in the child repositories describe stage 2 as if it were the present. The map says plainly that stage 1 is in scope, stage 2 is not, and the stage 2 text stays as the target. One decision (DECISIONS, W-002) removed a whole class of wrong turns.

## How to build the map with the agent

1. **Let the agent survey first.** Ask it to read the repositories and describe the system in its own words. Do not give it your description yet.
2. **Correct it.** Its survey will be partly wrong, and the wrong parts are exactly the gaps in your documentation. In this case study the agent's first survey got four things wrong, all because a document was out of date or missing ([chapter 9](09-case-study.md)).
3. **Fix the documents, not only the chat.** Each correction goes into a file, or the next session makes the same mistake.

## What a map holds

- A table of the parts: repository, what it is, where it runs, what it talks to.
- Where each kind of thing comes from: data, definitions, content.
- Modes of operation, if there are several (here: synthetic demo data and a live lab system).
- What is in scope now and what is not.
- The environments: hosts, how they are reached, where secrets live (never the secrets themselves).
- How to build and test each part, marked "runs anywhere" or "needs the lab".

The last point matters more than it looks. An agent working only on GitHub cannot run a test that needs a lab behind a VPN. If the map does not say so, the agent either skips the test silently or claims it passed.

## Common mistakes

- Writing the map from memory instead of from a survey of the code.
- Writing the target as the present.
- Leaving "TODO" lines in it. A TODO in a map is a guess waiting to happen. Either fill it or move it to OPEN-QUESTIONS.

## Exercise

Ask your AI agent to describe your system without help. Count what it gets wrong. For each error, find the document that misled it.
