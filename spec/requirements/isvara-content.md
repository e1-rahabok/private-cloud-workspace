# Requirements: isvara.io content

What isvara.io's pages, tools and calculators must do, and how each part is tested. isvara.io presents Agent E2's knowledge and holds none of its own ([intent](../intent.md); answer to Q-18 in the [interview, round 1](../interview-round-1.md)). The rest of this file is written from the [isvara.io plan](../design/isvara-revamp.md) in milestone M1. IDs are explained in the [glossary](../glossary.md).

### R-CONTENT-001 isvara.io's numbers are generated from Agent E2's catalog

Milestone: M8.

Source: answer to Q-18 ("isvara.io is just a website. It is not where knowledge is stored."); WD-036. Reason: the capacity calculator on isvara.io today was ported from an old spreadsheet and uses an overcommit ratio of 4 to 1, where Agent E2 says 3 to 1 ([tutorial, chapter 11](../../tutorial/11-trust-in-ai-written-content.md)).

- Given any number isvara.io uses about performance or capacity: a limit, a band, an overcommit ratio or a class of service
- When isvara.io is built
- Then the number is read from a module generated from Agent E2's catalog
- And no such number is written by hand in isvara.io's code

Test scenarios:
- T-CONTENT-001a (anywhere, automated by a check to write, checks/isvara_numbers.py): the generated module equals the catalog; a hand-written threshold constant in isvara.io's code fails the check.
