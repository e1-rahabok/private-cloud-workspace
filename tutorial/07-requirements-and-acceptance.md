# 7. Requirements and acceptance criteria

## From a goal to something checkable

"Connect the web app to the live system" is a direction. An agent cannot tell when it has finished, so it stops when the work looks finished. A requirement turns a piece of a goal into a statement someone can check. Its acceptance criteria say what must be observably true for it to count as met, and its test scenarios say exactly how that is shown.

## Two kinds of requirement

- **Functional requirements** say what the product does: "a stale value shows 'No data'".
- **Quality requirements** say how well it does it: how fast, how safe, how much it may cost, how long it may be down. They are written with numbers where a number exists, such as "the page shows its first result within 2 seconds", and the design meets them ([chapter 8](08-design.md)).

Quality requirements are the ones most often left out, because nobody asks for them until they fail. In this project the author's answer on the knowledge service's speed became one: "Time is less of a concern, as even minutes are better than human. Accuracy matters more. Streaming is not needed. If it's going to take minutes, how to inform user Agent E2 is not hung or dead?" The requirement that followed says an answer may take minutes, and the user always sees that Agent E2 is still working. The author's closing question is the input that shaped the design of the progress display ([chapter 8](08-design.md)).

## The format

Each requirement has an ID, a short title, its reason, its source, the behaviour written as Given, When, Then, and one or more test scenarios. Here is one from this project, slightly shortened, in the form of the workspace's [requirement format](../spec/requirements/README.md):

> **R-LIVE-015 A stale value shows "No data" at once**
>
> Why: PCM shows what the adapter publishes, and a value that stopped updating must never look current.
>
> Source: Q-WS-27; Q-WS-64; DESIGN-17.
>
> - Given the VCF vCommunity Adapter collects every 5 minutes
> - When the newest sample of a metric is more than 10 minutes old (one cycle plus a margin of one cycle) when PCM reads it
> - Then the current value shows "No data" in grey, with the time of the newest sample
> - And it is never shown as 0 or coloured green
>
> Test scenarios:
> - T-LIVE-015a (anywhere, automated by a unit test of PCM's live pages): a fake API returns samples ending 9 minutes ago for one cluster and 11 minutes ago for another. The first shows its value; the second shows "No data".
> - T-LIVE-015b (lab, automated by the lab test script): a powered-off lab VM, for which no new samples arrive. Its page shows "No data" with the time of the last sample.

A few things to notice:

- **The Why and Source lines.** The Why line gives the reason in one sentence, so a reader can judge the requirement without opening anything else. The Source line points at the input it came from: here the author's answer to Q-WS-27, "If the data is stale, say no data. No need to wait 15 minutes"; Q-WS-64, where the agent set the limit at 10 minutes at the author's request; and the design choice it applies. A source can also be a goal, a constraint or a principle. A requirement with no source is the agent's invention, and it gets questioned. A script fails the build if a source is missing or points at nothing ([tools/spec_check.py](../tools/spec_check.py)).
- **The reason, beside the requirement.** When the restructure began on 2026-11-28, 157 of the 202 requirements in this project cited a decision such as WD-015 in their source, and the reason sat in the decision log. A reader had to open a second file to learn why. The method puts the reason next to what it shaped. When one reason serves many requirements, it lives once, in the principle or constraint they all cite ([chapter 2](02-the-method.md)).
- **Failure cases are explicit.** What happens when data is missing, late or wrong is where agents guess most, so those cases get their own requirements.
- **The numbers are pinned.** "Stale" is defined as more than 10 minutes old; a test can measure that, and "too old" it could not. The number is the agent's design, derived from the author's input and from a constraint, the 5-minute cycle. Where a number is not yet known, the requirement says so and names the assumption it uses meanwhile.

## Acceptance criteria

The Then and And lines are the acceptance criteria. Each one can be observed and has two outcomes, met or not met, with no adjective left to judge: "shows 'No data' in grey" can be checked, where "handles stale data gracefully" cannot. A requirement whose criteria cannot be observed cannot be accepted, only liked.

A test scenario is narrower than its criteria. It fixes the data, the steps and the expected result, and it says where it runs. One requirement usually needs more than one scenario: here, a boundary pair at 9 and 11 minutes that runs anywhere with a fake, and a lab scenario for what a fake cannot prove. [Chapter 10](10-test-plan-and-traceability.md) shows how the scenarios of every requirement fit into one test plan.

The acceptance criteria are written together. The agent drafts them from the input; the person adds the cases the field knows and a draft misses, such as the powered-off VM above.

## Writing guidance

- Start from what a user sees. "The tab shows the last 24 hours" can be checked. "Integrate the API" cannot.
- Say what must not change: existing behaviour that stays, defaults that stay defaults.
- Keep each requirement to one behaviour. A requirement with five "and"s is usually three requirements.
- Write the reason in the person's words where they gave one, and in one plain sentence where the agent derived it.
- Let the agent draft and the person review. Reading a requirement takes a minute; untangling code built from a misunderstood goal takes hours.

## Approval on one page

A person cannot approve forty requirements spread over four files. In this project a script builds one review page per milestone from the requirement files: one line per requirement, with its ID, what it says and how many of its tests need the lab. The ID links to the full text. The person reads one page and approves it, or names the lines they reject. Because a script writes the page and a check compares it with the files, it cannot go stale.

## Definition of done

A milestone's definition of done is its list of requirement IDs. It is finished when every scenario of every listed requirement passes, or when the person has agreed in writing that a scenario stays manual. In this project the milestones in [ROADMAP.md](../ROADMAP.md) list their requirements and what they depend on.

## Exercise

Take one goal from your backlog. Write two requirements for it in Given, When, Then form, one of them about a failure case and one with a number in it. Give each a source and a reason, and one scenario that runs anywhere. Ask someone who knows the system which line they disagree with.
