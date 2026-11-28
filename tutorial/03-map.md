# 3. The map

## Purpose

Before any work, write down what the system is today: its parts, where each runs, what talks to what, and how each is built and tested. One page is enough. In this project the map is the first part of the design, [spec/design/system.md](../spec/design/system.md). The brief, [spec/brief.md](../spec/brief.md), says why each part exists, who it is for and what is in scope ([chapter 4](04-goals-and-scope.md)). The agent writes the map from a survey of the code, and the person corrects it.

## Keep today apart from tomorrow

The most useful thing a map does is separate what exists now from what is planned. Documents that mix the two mislead the agent. It reads "the model runs locally", finds code that calls a cloud model, and then either "fixes" the code or stops trusting the document.

This project has two futures. In the first, the product is a demo in the author's lab and the knowledge service calls a cloud model. In the second, a customer installs everything on their own hardware with a local model. Several documents described the second as if it were already true. One line on the map, saying the first is in scope and the second is not, stopped a whole class of wrong turns.

## Building the map with the agent

Ask the agent to read the repositories and describe the system in its own words, before you give it your description. Its account will be partly wrong, and the wrong parts point straight at the gaps in your documentation. In this project the first survey got four things wrong, each because a document was out of date or missing ([chapter 16](16-case-study.md) lists them).

Correct the documents, not only the conversation. Otherwise the next session makes the same mistake.

## Contents of the map

- A table of the parts: repository, what it is, where it runs, what it talks to.
- Where each kind of thing comes from: data, definitions, content.
- The modes the system runs in, if there are several. Here: demo data, and a live lab.
- Which parts of the plan exist now and which are still to come. The scope itself is in the brief.
- The environments: hosts, how they are reached, and where secrets are kept (never the secrets themselves).
- How to build and test each part, marked "runs anywhere" or "needs the lab".

That last point matters more than it seems. An agent that only works on GitHub cannot run a test that needs a lab behind a VPN. If the map does not say so, the agent either skips the test quietly or reports that it passed.

## Common mistakes

- Writing the map from memory instead of from a survey of the code.
- Describing the plan as if it were the present.
- Leaving "TODO" lines in it. Either fill them in or turn them into questions for the interview.

## Exercise

Ask your agent to describe your system without help. Count what it gets wrong, and for each error find the document that misled it.
