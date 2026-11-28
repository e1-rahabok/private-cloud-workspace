# Test plan

How release 1.0 is proven: what is tested, at which level, where each test runs, on which data, when a pull request and a milestone may pass, and how each test traces back to the author's input. Claude writes and runs the tests; the author sets the acceptance bar and approves each milestone. The test scenarios themselves are in the [requirements](requirements), one or more under each requirement. IDs are explained in the [glossary](glossary.md).

## Approach

- Every requirement has at least one test scenario, and every scenario names its requirement ([requirements/README.md](requirements/README.md), section Format).
- A scenario says where it runs, anywhere or in the lab, its data and steps, the expected result, and the test or check that automates it, or why it stays manual.
- A scenario that runs anywhere is preferred. A lab scenario is written only for what a fake cannot prove.
- A test is never weakened, skipped or deleted to pass. A failure is a bug to fix or a question for the author.
- A product with pages has a drawing of what its visitor sees: the site map, the menus, a rough mock of each page and the journeys through them. A journey test walks each journey across pages. isvara's is [visitor-experience.md](https://github.com/e1-rahabok/isvara/blob/main/spec/visitor-experience.md) with [journeys.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/journeys.md); PCM's are its demo scripts in [demo/README.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/demo/README.md), walked by [`demo/rehearse.mjs`](https://github.com/e1-rahabok/private-cloud-manager/blob/main/demo/rehearse.mjs).
- A repository with lab tests has its own test plan: the run order, the oracle that gives each expected value, safety, and what decides a pass. The adapter's is its [Live Validation Test Plan](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/validate/validate.md); PCM's is its [test plan](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/test-plan.md).
- A lab test that checks a value compares it with an oracle that shares no code with the system under test, such as PCM's reference script reading the Suite API itself.
- On 2026-11-28 the specification held 222 requirements and 339 test scenarios, 42 of them in the lab; `python tools/spec_check.py` prints the current totals.

## Test levels

| Level | Proves | Runs | When |
|---|---|---|---|
| Specification checks | Every requirement traced, tested, sourced; links and diagrams; writing rules | [`tools/`](../tools) | Every pull request |
| Unit tests | One part's logic, against fakes | Each repository's tests | Every pull request of that repository |
| Contract checks | Both sides of a contract agree; each planted break fails | [`contract-checks/`](../contract-checks) | Every pull request of every repository; daily |
| Page tests | A page renders and behaves, with stub services | PCM's Playwright page tests; isvara's build | Every pull request of that repository |
| Journey tests | A visitor's path through several pages leads where it should | isvara's journey tests on the Vercel preview, from M4; PCM's demo rehearsals, synthetic and live | Every pull request of isvara from M4; before every PCM demo |
| Model evaluations | Answers are right, cited and safe | Agent E2's graded answer set; isvara.io's two batteries | Each change of model or prompt |
| Lab tests | The system works on real VCF Operations data; PCM's values equal VCF Operations' | The adapter's `validate.ps1`; PCM's `Test-Live.ps1` ([test plan](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/test-plan.md)) | M8, in a session with the author |
| Acceptance | A milestone's outcome holds, as the author confirms it in plain words | The milestone's [review page](review), which carries no test counts | When the milestone's work is done |

- **Specification checks:** [spec_check.py](../tools/spec_check.py) (traceability, DESIGN-8), [milestone_review.py](../tools/milestone_review.py) (each requirement in one milestone), [milestone_gate.py](../tools/milestone_gate.py) (changes stay in the open milestone), [docs.py](../tools/docs.py) (links and diagram text), [style.py](../tools/style.py) (writing rules), [claude_md_copies.py](../tools/claude_md_copies.py) (one CLAUDE.md in every repository).
- **Review page:** [milestone_review.py](../tools/milestone_review.py) writes each milestone's page and fails when a page carries a test count, an ID or a path, or lacks a section; [test_milestone_review.py](../tools/test_milestone_review.py) plants each break (T-WS-015a). The author's first read of each page is the manual test (T-WS-015b).
- **Branch cleanup:** [branch_cleanup.py](../tools/branch_cleanup.py) is tested against a fake GitHub by [test_branch_cleanup.py](../tools/test_branch_cleanup.py) (T-WS-014a). On every pull request its workflow lists what it would delete, and the first real run in each repository is checked by hand (T-WS-014c).
- **Contract checks:** C1, C3 and C5 run today (C5 needs the gateway key); C2 is added in M8 and C4 in M4 ([system design](design/system.md), section Contracts). Each check has a test that plants a break of each kind it compares (R-WS-001).
- **Model evaluations:** Agent E2's free-text answer set, graded by a strong model as judge (DESIGN-19), about US$2 a run; isvara.io's citation eval and injection battery, against a running server (DESIGN-10); Agent E2's full multiple-choice round never runs (the author, 2026-11-28; DESIGN-31). Each run stops when its spending reaches US$100, and an answer or a grade whose inputs have not changed is reused (CONSTRAINT-1, DESIGN-31). All need the Vercel AI Gateway key (DEPENDENCY-2), which no GitHub workflow holds.

## Environments

- **Anywhere:** a cloud session or GitHub Actions, with the repositories cloned side by side. Every unit test, contract check, page test and specification check runs here.
- **With the gateway key:** the same, plus the Vercel AI Gateway key in the environment. Model evaluations run here, from M3 on.
- **The lab:** the author's laptop over the VPN, with PowerShell 7 and the adapter's build, install, restart and validation tools (CONSTRAINT-6). Only M8 runs here.
- **Lab tests before M8:** a cloud session runs every test that works with fakes, reports each check that needs the lab as not run, lists it in its pull request for M8's lab session, and goes on. M8's lab session runs every listed check. [milestone_review.py](../tools/milestone_review.py) fails when a lab scenario sits outside a milestone that runs in the lab.

## Test data

| Data | Used by | Kept in |
|---|---|---|
| Fakes of the Suite API and of Agent E2 | Unit and page tests | Each repository's tests |
| ACME, PCM's synthetic bank | PCM's demos 1 to 6 and page tests | PCM's generator |
| Agent E2 in mock mode, no model | Contract check C3 | agent-e2's answer service |
| Planted breaks | Each check's own test: contracts, names, lab addresses, secrets, workflows | `test_<check>.py` beside its check, in [`contract-checks/`](../contract-checks) or [`tools/`](../tools) |
| Free-text answer set, about 15 questions | Agent E2's graded evaluation | agent-e2's benchmark |
| 20 reader questions and an attack battery | isvara.io's two batteries | isvara's evals |
| The lab's VCF Operations and vCenter | Lab tests, read-only | The author's lab |

- No test reads customer data. Lab facts may go to the cloud model (SCOPE-5).
- A test that needs a credential reads it from the files of DESIGN-9 and never prints it.

## Entry and exit criteria

- **A pull request may merge** when every check its repository runs has reported and passed, and its text lists any lab check it could not run. Claude merges its own pull requests, and Dependabot's (DESIGN-25), once the checks pass.
- **A build milestone may start** when the milestone before it is approved and the repositories it changes run their own tests in CI (section Own tests in CI).
- **A milestone is done** when every test scenario of its requirements passes, every listed lab check has run (M8), its review page is current, and the author approves it (DEPENDENCY-1).
- **Release 1.0 is done** when the author approves M8 and the measures of GOAL-4 hold.

## Traceability

The chain from the author's input to the code, and the tool that checks each link (DESIGN-8):

| Link | Written in | Checked by |
|---|---|---|
| Answer to brief item | The brief item's Source | spec_check: every ID it names exists |
| Brief item to requirement | The requirement's Why and Source lines | spec_check: Why present; Source names an existing ID |
| Requirement to design choice | The design choice's Serves line | spec_check: every ID it names exists |
| Requirement to test scenario | Scenario ID `T-<area>-<nnn><letter>` | spec_check: one scenario at least, none orphaned |
| Requirement to milestone | ROADMAP.md, or the requirement's Milestone line | milestone_review: exactly one milestone |
| Scenario to automated test | "automated by" in the scenario | Not checked yet (Known gaps) |
| Contract to its check | The contracts table of the system design | spec_check: the check exists and runs |

## Own tests in CI

Each repository runs its own tests on every pull request and every push to main, beside the cross-repo checks:

| Repository | Workflow | Runs |
|---|---|---|
| agent-e2 | [tests.yml](https://github.com/e1-rahabok/agent-e2/blob/main/.github/workflows/tests.yml) | The rules check, the harness and runner unit tests, the project tools' tests |
| PCM-Adapter | [ci.yml](https://github.com/e1-rahabok/PCM-Adapter/blob/main/.github/workflows/ci.yml) | Unit tests, lint, security scan, dependency audit |
| private-cloud-manager | [tests.yml](https://github.com/e1-rahabok/private-cloud-manager/blob/main/.github/workflows/tests.yml) | Every unit test, then every page test, one after the other |
| isvara | [`.github/workflows/checks.yml`](../.github/workflows/checks.yml), in the private repository | Lint, type check, the RVTools test, the link gate, the build |

- Why: on 2026-11-28 PCM's L2 page test LPG-20 failed on main and nobody saw it, because only sessions ran it (RISK-7 in the [brief](brief.md)).
- A test that needs the lab or the gateway key stays out of CI (section Environments).

## Known gaps

- **Scenario to automated test:** a scenario names its test in prose ("automated by ..."), and no check confirms that the test exists. Every repository runs its own tests in CI since 2026-11-28 (section Own tests in CI), so the next step is that spec_check reads the named path of each scenario in a done milestone and fails when it does not exist.
- **isvara in the workspace's CI:** isvara is private, so the workspace's CI cannot read it; isvara runs the cross-repo checks in its own CI with the four public repositories checked out (R-WS-002).
- **Contracts without a check:** C2 and C4, planned in M8 and M4.

## Commands per repository

| Repository | Runs anywhere | Needs the lab or a key |
|---|---|---|
| agent-e2 | `python3 project/tools/rules_check.py`; unit tests of the harness and the benchmark runner | The benchmark needs the gateway key |
| PCM-Adapter | `python -m pytest tests`, from `Management Pack` | `pwsh tools/build/build.ps1`, `install.ps1`, `restart.ps1`, `validate.ps1` (the lab) |
| private-cloud-manager | Unit and page tests per workspace ([pcm/README.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/pcm/README.md)); `node demo/rehearse.mjs` | Install on the lab VM ([deploy/README.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/deploy/README.md)); `pwsh tools/lab/Test-Live.ps1`, to write ([test plan](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/test-plan.md)) |
| isvara | `npm run lint`, `typecheck`, `build`, `test:rvtools`; the journey tests on the Vercel preview, from M4 | `npm run eval` and `eval:injection` need a server and the key |
| All four together | `uv run contract-checks/run_all.py` (this repository) | |
