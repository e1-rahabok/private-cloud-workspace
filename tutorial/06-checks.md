# 6. Checks

## The idea

A contract between two parts is only real when code verifies it. Each seam in `CONTRACTS.md` gets a check: a script that reads both sides and fails when they disagree. It runs before every merge, on a schedule, and whenever someone asks.

The checks in this workspace are in [`checks/`](../checks). Each is short enough to read in a few minutes.

## Two kinds of check

**Compare definitions.** `kpi_definitions.py` (C1) reads the KPI definitions in Agent E2's catalog and the adapter's code, and compares them row by row: the five limits and one flag per sub-metric. It connects to nothing. It runs in a second.

**Exercise the real thing.** `agent_e2_api.py` (C3) starts the real Agent E2 service in mock mode (no model, no network), then calls each endpoint with the web app's own client code and checks every field the web app reads. It runs in about eight seconds. It tests the seam as it is used, not as it is documented.

Prefer the second kind when it is cheap enough. A check against documentation passes while the code has already moved on.

## Prove the check can fail

A check that never fails proves nothing. After writing one, plant a break and run it:

- For C1, one limit in the catalog was changed from 200 to 250. The check failed and named the row.
- For C3, one response field was renamed in the service. The check failed and named the field.

Then undo the plant. Ten minutes, and you know the check works.

## Baselines that only shrink

When a check is new, it often finds real gaps that cannot all be fixed today. C1 found 11 sub-metrics whose names differ between the catalog and the adapter (their limits agreed). Two bad options:

- Let the check fail until all 11 are fixed: it fails every day, and people learn to ignore it.
- Remove the check: the gaps grow.

The middle way is a **baseline**: the 11 known gaps are listed in the check, reported as KNOWN, and do not fail. Any new gap fails. A listed gap that has been fixed also fails until it is removed from the list. So the list can only shrink. Each known gap also has an entry in `OPEN-QUESTIONS.md` saying who decides the fix.

## Where checks run

- Locally, with one command: `uv run checks/run_all.py`.
- In GitHub Actions on every push and pull request to this repository, daily, and on demand.
- Later (ROADMAP, M1), on every pull request in each child repository, so a break is caught before it merges rather than the next morning.

## Rules for the agent

- Never weaken a check to make it pass.
- A new known gap goes into a baseline only with an entry in OPEN-QUESTIONS.
- A new contract gets a check, or a roadmap line that adds one.

## Exercise

Pick one seam from chapter 4's exercise. Write a check that reads both sides and compares one thing. Plant a break. Did it fail?
