# 10. Test plan and traceability

## Purpose

Each requirement has its test scenarios ([chapter 7](07-requirements-and-acceptance.md)). The test plan shows how all of them fit together: the levels of testing, where each level runs, what data it uses, who or what runs it and when, and what must pass before a milestone counts as done. Without a plan, every scenario is written well and the whole still has gaps: a level nobody runs, data nobody owns, a lab test that waits forever.

The plan is written together. The agent drafts the levels, the environments and the tools. The person adds what only the field knows: realistic data, the cases that break in real estates, and what a demo audience will try first. In this project the plan is [spec/test-plan.md](../spec/test-plan.md).

## Levels

Each level proves something the others cannot. The examples are this project's.

| Level | What it proves | Example |
|---|---|---|
| Unit | One module does its job | PCM's unit tests; the adapter's tests with a fake API |
| Contract | Both sides of a seam agree | The KPI definitions check; the Agent E2 API check |
| Specification | The documents are complete and linked | Every requirement has a source and a test |
| Page | What a user sees works | PCM's page tests in a headless browser |
| Evaluation | A model's answers are right | Agent E2's benchmark and retrieval check |
| Lab | The product works on the real system | The adapter's live validation against VCF Operations |
| Review | What no script can judge | A slogan in a document; a demo walk-through |

A level is chosen by what it costs and what it catches. A unit test runs in a second and catches a broken function. The contract check runs in eight seconds and catches a renamed field that both sides' unit tests miss ([chapter 11](11-checks.md)). A lab test needs the author's laptop and catches what no fake can, such as a metric key the real API does not return.

## Environments

Every scenario says where it runs: "anywhere", on any machine with fakes, or "lab", on the real VCF Operations behind the author's VPN. The plan decides when each kind runs:

- **Anywhere:** on every pull request in every repository, once a day, and on demand.
- **Lab:** only in milestone M8, the one milestone that runs in the lab. Before M8, a session reports each lab test as "not run", lists it in its pull request, and goes on. A test that was not run is never reported as passed.

## Test data

Name the data each level uses, and who keeps it true.

- **Synthetic data with known answers.** PCM's demo customer, ACME Corp, is generated from a fixed specification, so every expected number is known before the code runs. Each regeneration of the code is checked against those numbers.
- **Fakes.** A fake Suite API answers the way VCF Operations does, including the failures: one scenario has it return an error for the second batch of objects, to prove the adapter publishes nothing built from half a read.
- **Boundaries.** A pair on each side of a limit catches an off-by-one: samples 9 and 11 minutes old around the 10-minute limit for stale data.
- **Planted breaks.** Each check has a test that breaks one side on purpose and expects the check to fail ([chapter 11](11-checks.md)).
- **Real data.** The lab supplies what no fake can. A lab test only reads, unless its milestone says otherwise and the person agrees.

## Entry and exit

- **Entry:** a milestone's build starts when its requirements are approved on its review page ([chapter 7](07-requirements-and-acceptance.md)).
- **Exit:** a milestone is done when every scenario of every requirement in it passes, or when the person has agreed in writing that a scenario stays manual.
- **Failures:** a failing test is a bug to fix or a question for the person. It is never weakened, skipped or deleted to get a pass.
- **Known gaps:** a gap that cannot be fixed at once goes into the check's baseline, with an open question, and the baseline may only shrink.

## Traceability

Traceability is the chain from why to proof. Each link is an ID, so a script can follow it:

- a goal or a constraint in the brief (GOAL-1, CONSTRAINT-2);
- the requirement that serves it (R-LIVE-015);
- the design choice that meets it (DESIGN-3);
- the test scenarios that prove it (T-LIVE-015a, T-LIVE-015b);
- the test code each scenario names;
- the result of the last run.

With the chain in place, three questions can be answered from the files alone. Why does this code exist? Follow it up. What breaks if this goal changes? Follow it down. Is the milestone done? Count the results at the bottom.

Part of the chain is checked by script in this project today. [tools/spec_check.py](../tools/spec_check.py) fails a requirement with no source or no scenario, and a scenario with no requirement. [tools/milestone_review.py](../tools/milestone_review.py) fails a requirement that sits in no milestone or in two, and a lab scenario outside the lab milestone.

The links nearest the code are the newest. 131 of the 309 scenarios name a test that is still to write. That is expected before their milestones are built. At the end of a milestone, a script should confirm that each named test exists and passed; until then, a scenario that names an unwritten test reads like coverage in a list.

## Division of work

- The agent drafts the levels, the environments, the tools and the traceability checks, and keeps the plan in step with the requirements.
- The person adds realistic data and the failure cases the field knows, and agrees which scenarios stay manual.
- Both read the result at the end of each milestone.

## In VMware terms

This is the test plan of a design, signed off before the build: what is tested, how, in which environment, and what counts as a pass. The traceability chain is the matrix that maps each requirement to its design decision and its test.

## Exercise

Take one requirement of your own and write its chain: the goal it serves, the design choice that meets it, two scenarios at different levels, and the name of each test. Mark the links that no script checks.
