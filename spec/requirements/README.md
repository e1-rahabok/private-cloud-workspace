# Requirements

One file per area. Each requirement is one testable statement with its own ID, and at least one test scenario. A requirement that cannot be tested as written goes back to [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md).

## Files (planned)

| File | Area | Milestone |
|---|---|---|
| `kpi-definitions.md` | One KPI definition across Agent E2, the VCF vCommunity Adapter and PCM | M2 |
| `pcm-live.md` | PCM reading the lab VCF Operations | M6, M7 |
| `agent-e2-service.md` | What Agent E2 answers, for PCM and isvara.io | M6, M9 |
| `isvara-content.md` | isvara.io pages generated from the Agent E2 knowledge base | M8 |
| `isvara-agent.md` | Agent E2 in place of AskIO | M9 |
| `isvara-exam.md` | The exam for people | M10 |

## Format

```markdown
### R-LIVE-003 Missing data is never shown as healthy

Source: OPEN-QUESTIONS answer to Q-12; PCM D-041.

Given a cluster whose Cluster Performance has no sample in the last 20 minutes
When the L2 Performance tab of that cluster opens in demo scenario 7
Then the KPI shows "stale" with the time of the last sample
And it is not coloured green and not shown as 0

Test scenarios:
- T-LIVE-003a (lab, automated by build/tests/test_live.py::test_stale_cluster): stop collection on one lab
  cluster's adapter instance for 25 minutes; open the tab; expect "stale" and the last sample time.
- T-LIVE-003b (anywhere, automated by build/tests/test_live.py::test_stale_fake): a fake Suite API whose
  newest sample is 21 minutes old; expect the same.
```

Rules:

- The ID never changes once used. A dropped requirement keeps its ID with the word "Dropped" and the reason.
- `Source:` names the answer or decision it comes from. No source, no requirement.
- Each test scenario says where it runs (anywhere, or the lab), the data and steps, the expected result, and the test or check that automates it, or why it stays manual.
- A scenario that runs anywhere is preferred. A lab scenario is added only for what a fake cannot prove.
