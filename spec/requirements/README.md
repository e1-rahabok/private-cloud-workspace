# Requirements

One file per area. Each requirement is one testable statement with its own ID, and at least one test scenario. This folder holds the requirements on the contracts between repositories, their checks and the workspace's tools. Every other requirement is in the repository that implements it (WD-036), in the folder named by [tools/requirement_files.py](../../tools/requirement_files.py): project/requirements in agent-e2, and spec/requirements in PCM-Adapter, private-cloud-manager and isvara. The tools read them all from clones next to this repository. A requirement that cannot be tested as written goes back to [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md).

## Files

The files and their status: [spec/README.md](../README.md), section Status.

## Format

```markdown
### R-AREA-001 Missing data is never shown as healthy

Source: OPEN-QUESTIONS answer to Q-WS-12; PCM D-041.

Given a cluster whose Cluster Performance has no sample in the last 20 minutes
When the L2 Performance tab of that cluster opens in demo scenario 7
Then the KPI shows "stale" with the time of the last sample
And it is not coloured green and not shown as 0

Test scenarios:
- T-AREA-001a (lab, automated by build/tests/test_live.py::test_stale_cluster): stop collection on one lab
  cluster's adapter instance for 25 minutes; open the tab; expect "stale" and the last sample time.
- T-AREA-001b (anywhere, automated by build/tests/test_live.py::test_stale_fake): a fake Suite API whose
  newest sample is 21 minutes old; expect the same.
```

Rules:

- The ID never changes once used. A dropped requirement keeps its ID with the word "Dropped" and the reason.
- `Source:` names the answer or decision it comes from. No source, no requirement.
- Each test scenario says where it runs (anywhere, or the lab), the data and steps, the expected result, and the test or check that automates it, or why it stays manual.
- A scenario that runs anywhere is preferred. A lab scenario is added only for what a fake cannot prove.
