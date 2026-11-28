# Test plan

How every requirement is proven: the levels of testing, where each runs, the data each uses, and what a milestone needs to pass. The agent drafts it; the person adds realistic data and the failure cases the field knows.

## Levels

| Level | What it proves | Command or tool | When it runs |
|---|---|---|---|
| Unit | One module does its job | | Every pull request |
| Contract | Both sides of a seam agree | | Every pull request, daily |
| Specification | Every requirement has a source and a test | | Every pull request |
| Page | What a user sees on one page works | | Every pull request |
| Journey | A user's path across pages leads where it should, one test per journey in DESIGN.md | | Every pull request |
| Special environment | The product works on the real system | | <milestone> |
| Review | What no script can judge | A reader | Before merge |

## Environments

| Environment | What runs there | Who can reach it |
|---|---|---|
| Anywhere | Every scenario marked "anywhere", with fakes | Any machine and the CI |
| <lab> | Every scenario marked "lab" | <who, and how> |

- Before the milestone that runs in <lab>: report each lab scenario as not run, list it in the pull request, and go on. Never report it as passed.

## Test data

- Synthetic data with known answers: <what it is, and where its expected numbers live>
- Fakes: <each fake, and the failures it can return>
- Boundaries: <a value on each side of each limit>
- Planted breaks: <one per check, kept as a test>

## Lab run order

A repository with tests in a special environment keeps this section, or its own test plan with the same parts.

| Step | What it checks | Scenarios | On failure |
|---|---|---|---|
| 1. Access | <the environment answers, sign-ins work> | | Stop |
| 2. <inputs exist> | <every key or field the product reads is there and fresh> | | Stop |
| 3. <values> | <each value equals the oracle's> | | Go on |
| <n>. End to end | <the whole demo or user path, step by step> | | Go on |

- A step whose condition fails stops the run; every later scenario is reported as not run.
- Each scenario prints its ID, PASS, FAIL or NOT RUN, and a short detail. The run fails when any scenario failed or did not run.
- Safety: <read-only calls, the account used, where its credential lives; nothing printed or saved>.

## Oracle

- The second source of each expected value: <the script or system, and what it reads>.
- It shares no code with the system under test.
- It is tested itself on data with known answers: <T- ID>.

## Entry and exit

- Entry: a milestone's build starts when its requirements are approved.
- Exit: every scenario of every requirement in the milestone passes, or the person has agreed in writing that it stays manual.
- A failing test is a bug to fix or a question for the person. Never weaken, skip or delete it.
- A known gap goes into the check's baseline with an open question. The baseline may only shrink.

## Traceability

- Chain: GOAL or CONSTRAINT, then R-, then DESIGN-, then T-, then the test code, then the result.
- Checked by: <script>: <which links>.
- Not yet checked: <links, and the milestone that adds a check>.
