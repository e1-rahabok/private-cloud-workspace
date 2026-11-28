# Requirements

One file per area. Each requirement is one testable statement with its own ID, and at least one test scenario. This folder holds the requirements on the contracts between repositories, their checks and the workspace's tools. Every other requirement is in the repository that implements it (DESIGN-4), in the folder named by [tools/requirement_files.py](../../tools/requirement_files.py): project/requirements in agent-e2, and spec/requirements in PCM-Adapter, private-cloud-manager and isvara. The tools read them all from clones next to this repository. A requirement that cannot be tested as written goes back to [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md).

## Files

The files and their status: [spec/README.md](../README.md), section Status.

## Format

```markdown
### R-AREA-001 Missing data is never shown as healthy

Why: green on a cluster with no data sends the operator away from the cluster that needs attention.

Source: Q-WS-12; DESIGN-17.

Given a cluster whose Cluster Performance has no sample in the last 20 minutes
When the L2 Performance tab of that cluster opens in demo scenario 7
Then the KPI shows "stale" with the time of the last sample
And it is not coloured green and not shown as 0

Test scenarios:
- T-AREA-001a (lab, automated by pcm/l2/tests/test_live.py::test_stale_cluster): stop collection on one lab
  cluster's adapter instance for 25 minutes; open the tab; expect "stale" and the last sample time.
- T-AREA-001b (anywhere, automated by pcm/l2/tests/test_live.py::test_stale_fake): a fake Suite API whose
  newest sample is 21 minutes old; expect the same.
```

Rules:

- The ID never changes once used. A dropped requirement keeps its ID with the word "Dropped", its Source and the reason, and needs no Why line or scenario.
- `Why:` gives the reason in one line, so a reader can judge the requirement without opening its source. The answer's outcome lives here and in the brief, with no separate decision log (DESIGN-8).
- `Source:` names the IDs it comes from: an answer (Q-WS-), a brief item (GOAL-, SCOPE-, CONSTRAINT- and the rest) or a design choice (DESIGN-). No source, no requirement.
- A later answer changes the requirement in place; git keeps the history.
- Each test scenario says where it runs (anywhere, or the lab), the data and steps, the expected result, and the test or check that automates it, or why it stays manual.
- A scenario that runs anywhere is preferred. A lab scenario is added only for what a fake cannot prove.
