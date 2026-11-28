# 9. Seams and owners

## Seams

A seam is any place where two parts depend on each other: an API call, a file one part writes and another reads, a definition two parts must agree on. Bugs gather at seams, because each side is tested on its own and nobody tests where they meet. The contracts at the seams are part of the design ([chapter 8](08-design.md)), and the agent writes them.

List every seam as a contract, with these fields. In this project the contracts C1 to C5 are a section of the design, [spec/design/system.md](../spec/design/system.md):

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

In this project the documents disagreed about who owned the performance definitions. One repository said its knowledge base was the only master; another said its own metrics were the definitions; a third followed the knowledge base. The agent found the disagreement and asked the author where the knowledge belongs. The author's input settled it: "Isvara.io should never have its own knowledge. Fix it. It should be aligned with Agent E2". The design followed from that input: Agent E2's catalog is the master, the management pack implements it, the web apps consume it, and the contract check compares the copies ([WD-001](https://github.com/e1-rahabok/private-cloud-workspace/blob/8677e71/DECISIONS.md#wd-001-agent-e2-as-the-source-of-domain-knowledge) recorded it as a decision at the time).

Once a master is chosen, check it first whenever two copies disagree. In this project a new design document listed the operations topics with "configuration" where the knowledge service had "value". The agent proposed changing the knowledge service to match. The knowledge service was right: it follows the framework the author wrote. The newer document was the copy that had drifted.

## The parent repository's territory

The parent repository specifies the seams and nothing inside the parts. In this project its requirements once said that the knowledge service's catalog "defines the scoring rules", and they restated a capacity formula. Both belonged elsewhere. The formula is domain knowledge, kept in the knowledge service. The scoring code, and its tests, belong to the management pack that runs it. The catalog is a list of numbers that the management pack's tables must equal. A requirement on a seam says that two sides are equal, and names the check that compares them.

## Changing a seam safely

A contract changes in three steps:

1. The owner adds the new shape and keeps the old one working.
2. Each consumer moves to the new shape.
3. The owner removes the old shape.

The checks pass after every step, so a change in one repository never breaks another.

A field that no consumer fills is a promise nobody tests. The knowledge service read a `production` flag to choose between two closure levels, and its contract listed the flag, but no caller ever sent it. Every cluster was judged at the production level, and the explanation called it "the production limit" even for a test cluster. The author's answer, that release 1.0 knows nothing about a cluster's environment, removed the flag; the explanation now says that every cluster gets the production limit, and why. When a contract lists a field, check that some consumer sends it.

A document's layout is a contract too, once a tool reads it. The specification check found the product's decision numbers by reading the rows of a table. When the decision log became one block per decision, the change kept a short index table at the top, so every repository's checks still passed; the check then moved to the block headings. Those are the same three steps.

## Exercise

Draw your system's parts as boxes, and a line wherever two parts depend on each other. Name the owner of each line. A line without an owner is a decision you have not made yet.
