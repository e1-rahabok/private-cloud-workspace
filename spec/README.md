# Specification

What the product must do, and how each part of that is tested. Built in M1 from the author's answers to the interview, before any build milestone starts. The plan on one page is [ROADMAP.md](../ROADMAP.md). IDs are explained in the [glossary](glossary.md).

## Five layers

| Layer | Answers | Where |
|---|---|---|
| 1. Intent | Why the product exists, success, failure, principles | [intent.md](intent.md) |
| 2. Requirements | What each part must do, each with its tests | [requirements/](requirements) |
| 3. Contracts | How the repositories meet | [CONTRACTS.md](../CONTRACTS.md) |
| 4. Decisions | What is settled, and why | [DECISIONS.md](../DECISIONS.md) |
| 5. Checks | The code that proves layers 2 and 3 | [checks/](../checks), [tools/](../tools), each repository's tests |

## Supporting files

- [knowledge-model.md](knowledge-model.md): the three learning paths, the four lenses, depth, experience and scale.
- [design/isvara-revamp.md](design/isvara-revamp.md): the isvara.io plan. [design/fine-tuning.md](design/fine-tuning.md): why the model is not fine-tuned in release 1.0.
- [interview-round-1.md](interview-round-1.md) and [interview-round-2.md](interview-round-2.md): the interview, with the author's answers and the decisions taken at his request. The questions still open are in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md).
- [glossary.md](glossary.md): every ID and short name.

## Status

| File | Requirements | Status |
|---|---|---|
| [workspace.md](requirements/workspace.md) | 6 | M2: ready for approval |
| [kpi-definitions.md](requirements/kpi-definitions.md) | 8 | M2 (001 to 007): ready for approval |
| [repositories.md](requirements/repositories.md) | 6 | M2: ready for approval |
| [pcm-adapter.md](requirements/pcm-adapter.md) | 24 | M2 part (005 to 012): ready for approval; the rest to update |
| [lab-build.md](requirements/lab-build.md) | 4 | After release 1.0 (WD-031) |
| [agent-e2-service.md](requirements/agent-e2-service.md) | 19 | To update for round 2 and WD-026 |
| [pcm-live.md](requirements/pcm-live.md) | 32 | To update for round 2 |
| [isvara-exam.md](requirements/isvara-exam.md) | 13 | To update for round 2 |
| isvara.io content, Ask, contributions, practice | none yet | To write from the [isvara.io plan](design/isvara-revamp.md) |

`python tools/spec_check.py` prints the current totals and fails on a requirement with no source or no test, or a test with no requirement.
