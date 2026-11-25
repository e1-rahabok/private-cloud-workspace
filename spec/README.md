# Specification

What the product must do, and how each part of that is tested. Built in M1 from the author's answers to the interview, before any build milestone starts ([ROADMAP.md](../ROADMAP.md)). IDs are explained in the [glossary](glossary.md).

## Five layers

| Layer | Answers | Where |
|---|---|---|
| 1. Intent | Why each app exists, for whom, what success looks like, what is not done | [intent.md](intent.md) |
| 2. Requirements | What each part must do, one testable statement each, with its test scenarios | [requirements/](requirements) |
| 3. Contracts | How the repositories meet | [CONTRACTS.md](../CONTRACTS.md) |
| 4. Decisions | What is settled, and why | [DECISIONS.md](../DECISIONS.md) |
| 5. Checks | The code that proves layers 2 and 3 | [checks/](../checks), [tools/](../tools) and each repository's tests |

Supporting files:

- [interview-round-1.md](interview-round-1.md): the first interview, with the author's answers as written. Round 2 is in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md).
- [design/](design): design notes that need the author's review before requirements are written: the [isvara.io plan](design/isvara-revamp.md) and [fine-tuning](design/fine-tuning.md).
- [glossary.md](glossary.md): every ID and short name.

## Status

| File | Requirements | Test scenarios | Status |
|---|---|---|---|
| [requirements/workspace.md](requirements/workspace.md) | 5 | see the check | Ready for approval |
| [requirements/kpi-definitions.md](requirements/kpi-definitions.md) | 8 | see the check | Ready for approval |
| [requirements/pcm-adapter.md](requirements/pcm-adapter.md) | 24 | see the check | Waits for Q-72 to Q-89 |
| [requirements/lab-build.md](requirements/lab-build.md) | 4 | see the check | Waits for Q-119 to Q-122 |
| [requirements/agent-e2-service.md](requirements/agent-e2-service.md) | 19 | see the check | Waits for Q-57, Q-90 to Q-99 |
| [requirements/pcm-live.md](requirements/pcm-live.md) | 32 | see the check | Waits for Q-63 to Q-71 |
| [requirements/isvara-exam.md](requirements/isvara-exam.md) | 13 | see the check | Waits for Q-109 to Q-118 |
| isvara.io content and Agent E2 on isvara.io | none yet | | Written after the author's replies in [design/isvara-revamp.md](design/isvara-revamp.md) |

`python tools/spec_check.py` prints the current totals and fails on a requirement with no source or no test, or a test with no requirement.
