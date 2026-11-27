# 5. Seams and owners

## Seams

A seam is any place where two parts depend on each other: an API call, a file one part writes and another reads, a definition two parts must agree on. Bugs gather at seams, because each side is tested on its own and nobody tests where they meet.

List every seam in [CONTRACTS.md](../CONTRACTS.md), with these fields:

| Field | Meaning |
|---|---|
| Owner | The part that defines the shape |
| Consumers | The parts that depend on it |
| Shape | Where the exact definition is written |
| Check | The script that proves both sides agree |
| Status | Running, planned (with its milestone), or none (with the reason) |

This project has five seams. Two of them only became visible once they were written down.

The first was one definition held in three places. The knowledge service defines each performance score and its limits; the management pack computes the scores with its own copy of the limits; the web app shows them using a third copy of the names. Nobody thought of this as an interface, so nobody checked it.

The second was an API hidden by its own error handling. The web app turns any failure from the knowledge service into a polite "unavailable" on screen. That is good for users, but it also meant a renamed field would show up as "unavailable" rather than as an error anyone would notice.

## Owners

- When a fact exists in more than one place, decide which copy is the master. The others are then generated from it or checked against it. Without that decision, each copy is edited by a different session and they drift apart.

In this project the documents disagreed about who owned the performance definitions. One repository said its knowledge base was the only master; another said its own metrics were the definitions; a third followed the knowledge base. Only the author could settle that, and did: knowledge starts in the knowledge service, the management pack implements it, the web apps consume it ([DECISIONS](../DECISIONS.md), WD-001). The agent's part was to find the disagreement and put it to the author.

Once a master is chosen, check it first whenever two copies disagree. In this project a new design document listed the operations topics with "configuration" where the knowledge service had "value". The agent proposed changing the knowledge service to match. The knowledge service was right: it follows the framework the author wrote. The newer document was the copy that had drifted.

## Changing a seam safely

A contract changes in three steps:

1. The owner adds the new shape and keeps the old one working.
2. Each consumer moves to the new shape.
3. The owner removes the old shape.

The checks pass after every step, so a change in one repository never breaks another.

## Exercise

Draw your system's parts as boxes, and a line wherever two parts depend on each other. Name the owner of each line. A line without an owner is a decision you have not made yet.
