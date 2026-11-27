# 6. Requirements and tests

## From a goal to something checkable

"Connect the web app to the live system" is a direction. An agent cannot tell when it has finished, so it stops when the work looks finished. A requirement turns a piece of the goal into a statement someone can check, and a test scenario says exactly how.

## Start with intent

Before the requirements, write down for each part of the system who it is for, what success looks like and what it will not do ([spec/intent.md](../spec/intent.md)). In this project the author's answer to "what makes release 1.0 a success?" was: colleagues and customers who see the demo want to fork it and deploy it in their own environment. That one sentence later decided several design questions, because each option could be measured against it.

## The format

Each requirement has an ID, a short title, the answer or decision it comes from, the behaviour written as Given, When, Then, and one or more test scenarios. Here is one from this project, slightly shortened:

> **R-LIVE-015 A stale value shows "No data" at once**
>
> Source: the author's answer to Q-27; decision WD-015.
>
> Given the management pack collects every 5 minutes
> When the newest sample of a metric is more than 10 minutes old when the web app reads it
> Then the current value shows "No data" in grey, with the time of the newest sample
> And it is never shown as 0 or coloured green
>
> Test scenarios:
> - T-LIVE-015a (anywhere): a fake API returns samples ending 9 minutes ago for one cluster and 11 minutes ago for another. The first shows its value; the second shows "No data".
> - T-LIVE-015b (lab): a powered-off lab VM, for which no new samples arrive. Its page shows "No data" with the time of the last sample.

A few things to notice:

- **The source line.** Every requirement points at the answer or decision it came from. A requirement with no source is the agent's invention, and it gets questioned. In this project a script fails the build if a source is missing or points at nothing ([tools/spec_check.py](../tools/spec_check.py)).
- **Failure cases are explicit.** What happens when data is missing, late or wrong is where agents guess most, so those cases get their own requirements.
- **Each scenario says where it runs.** "Anywhere" means on any machine, with fakes. "Lab" means it needs the real environment. Prefer "anywhere" when a fake is cheap and honest, and keep a lab scenario for what a fake cannot prove.
- **The numbers are pinned.** "Stale" means more than 10 minutes, not "too old". Where the number was not yet agreed, the requirement says so and links to the open question.

## Writing guidance

- Start from what a user sees. "The tab shows the last 24 hours" can be checked. "Integrate the API" cannot.
- Say what must not change: existing behaviour that stays, defaults that stay defaults.
- Keep each requirement to one behaviour. A requirement with five "and"s is usually three requirements.
- Let the agent draft and the person review. Reading a requirement takes a minute; untangling code built from a misunderstood goal takes hours.

## Definition of done

A milestone's definition of done is its list of requirement IDs. It is finished when every scenario of every listed requirement passes, or when the person has agreed in writing that a scenario stays manual. In this project the milestones in [ROADMAP.md](../ROADMAP.md) list their requirements and what they depend on.

## Exercise

Take one goal from your backlog. Write two requirements for it in Given, When, Then form, one of them about a failure case, each with one scenario that runs anywhere. Ask someone who knows the system which line they disagree with.
