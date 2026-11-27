# Interview, round 4

Questions asked in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) on 2026-11-27, with the author's answers as written and what follows from each. IDs are explained in the [glossary](glossary.md).

## Q-WS-134 PCM's folders by workspace or by phase

PCM's folders follow the phase of work: [spec](https://github.com/e1-rahabok/private-cloud-manager/tree/main/spec), [design](https://github.com/e1-rahabok/private-cloud-manager/tree/main/design), the application code, deploy. One workspace such as L2 is spread over six folders: its design note, its API, catalog and test specifications, its code and its tests. Agent E2 instead groups by subject ([knowledge](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge)), so one folder holds the context of one task. R-REPO-007 renames PCM's folders without moving files between them.

- **Option A, keep the phases:** no move; a session gathers each workspace from six places.
- **Option B, one folder per workspace** (L2, NOC, capacity, docs, executive), each with its design, specifications, code and tests, plus one shared folder for the core: one folder is the whole context of a task, at the cost of moving several dozen files and updating every import and path.
- **Recommendation:** B, done after R-REPO-007 and before M6, the first milestone that builds PCM's live demo.

**Answer:** "Yes, by workspace."

**Result:** PCM's folders are grouped by workspace in M2, in the same change as the renames of R-REPO-007, so no file moves twice ([R-REPO-008](requirements/repositories.md)).
