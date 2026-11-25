# 4. Seams and owners

## Seams

A seam is any place where two parts meet: an API call, a file one part writes and another reads, a definition that two parts must agree on. Bugs collect at seams, because each side is tested on its own and nobody tests the meeting.

List every seam in `CONTRACTS.md`. For each one:

| Field | Meaning |
|---|---|
| Owner | The side that defines the shape |
| Consumers | The sides that depend on it |
| Shape | Where the exact definition is written |
| Check | The code that proves both sides agree |
| Status | Running, planned (with milestone), or none (with the reason) |

This workspace has five seams. Two of them were not obvious until written down:

- **The same definition in three places.** Agent E2's catalog defines each KPI's parts and limits. PCM-Adapter computes the KPIs with its own copy of those limits. PCM shows them with a third copy of the names. Nothing called this an interface, so nothing checked it.
- **An API hidden by error handling.** PCM's client turns any failure from Agent E2 into "unavailable" so the screen can say so politely. That same politeness would hide a broken contract: a renamed field shows up as "unavailable", not as an error.

## Owners

When a fact exists in more than one place, decide which copy is the master. Every other copy is then generated from it or checked against it. Without that decision, each copy gets edited by a different session, and they drift.

In this workspace the documents disagreed about who owned the KPI definitions. One repository said "the knowledge base is the one master". Another said "the adapter's metrics are our definitions". A third followed the knowledge base. Only the author could settle it, and did: knowledge starts in Agent E2, the adapter implements it, the web app consumes it (DECISIONS, W-001).

Notice that this was a question for the human, not the agent. The agent's job was to find the conflict and ask.

## Changing a seam safely

A contract changes in three steps:

1. **Expand.** The owner adds the new shape and keeps the old one working.
2. **Migrate.** Each consumer moves to the new shape.
3. **Contract.** The owner removes the old shape.

The checks pass after every step, so no repository is ever broken by another.

## Exercise

Draw your system's parts as boxes. Draw a line for every place two parts depend on each other. For each line, name the owner. Any line without an owner is a decision you still need to make.
