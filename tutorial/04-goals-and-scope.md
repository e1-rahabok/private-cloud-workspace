# 4. Goals and scope

## Purpose

Before any requirement, write down what the product must achieve, for whom, how anyone will know it worked, and what it will not do. Every later choice is measured against this page. When two designs both look reasonable, the goals decide between them; when the plan grows, the scope shows what does not belong.

This is the person's input. Only the domain expert knows the users, the problem and what would count as success. The agent's part is to ask, to write the answers down in the person's own words, and to point out a goal that nobody could measure.

In this project the goals and scope open the brief, [spec/brief.md](../spec/brief.md). The same file holds the constraints, assumptions, risks and dependencies of [chapter 6](06-constraints-assumptions-risks-dependencies.md), because the author prefers one file to a trail of links.

## Contents

- **The problem.** What goes wrong today, and for whom.
- **Goals.** The outcomes the product must bring about, each with an ID such as GOAL-1.
- **Users.** Who uses each part, and what they already know.
- **Success.** How each goal is measured, by whom, and when.
- **Failure.** What would make the product fail even if every requirement passed.
- **Scope.** What is in this release, and what is out, each with its reason. IDs such as SCOPE-1.
- **Principles.** Rules that settle a conflict between two good things without asking anyone. IDs such as PRINCIPLE-1.

## The problem

A good problem statement names a cost someone pays today. This project's is short: the author's material "lands only when the author explains or demonstrates it, and that does not scale". Everything else follows from it. The software exists so that customers can use the knowledge without the author, and the test of every part is whether a customer gets value without the author.

## Goals as outcomes

A goal describes a change in the world. "Rebuild isvara.io" is a task. "isvara.io is recognised worldwide as the authority on large-scale private cloud performance and capacity management" is an outcome, and the rebuild is one way to reach it. Writing the outcome matters because a task can be finished while the outcome is missed. This project's goals are outcomes of that kind: VMware administrators have the author's knowledge inside their own private cloud, and isvara.io is recognised as the authority. Release 1.0 is the first step toward both.

## Measures

A goal without a measure cannot tell you when you are done, or when to stop. This project's measures of authority are concrete: isvara.io's position in search results for about 20 searches that define the field, returning visitors, questions asked, and contributions from the vCommunity once they open.

Other statements of success are judgements, such as customers who see the PCM demo and "find it useful and want to copy the repositories privately". A judgement still works as a measure when someone is named to make it at a set time. A count works better: the number of colleagues who ask for the repositories after a demo can be tracked from the first demo onward.

## Failure

Failure statements catch what the goals miss. In this project each one sits beside the item it protects. The reason given for GOAL-3, value without the author, protects all the others: "every requirement can pass and the product still fail if a customer needs the author". PRINCIPLE-2, accurate before complete, sets a priority that shaped the design of the knowledge service: "A confident wrong answer is worse than none; Agent E2 fails if it gives one". Saying "I don't know" is acceptable, as it is from an expert.

## Scope and non-goals

Scope says what is in the release and what is out, each with its reason. The reason is what keeps an out-of-scope item out when someone argues for it later. Two examples from this project:

- **Day 2 only.** Running, monitoring, troubleshooting and planning are in. Design, installation, configuration and upgrades are out, because Day 1 knowledge changes with each release and release 1.0 must be small enough to finish. Agent E2 says so when asked and points to Broadcom's documentation.
- **Release 1.0 in the lab.** The product is a lab demo with a cloud model. The customer's own installation with a local model comes later. Before this line was written, sessions kept building toward the later deployment ([chapter 3](03-map.md)).

A non-goal is as useful to the agent as a goal. Without "the customer's own installation comes later", an agent that finds the words "local model" in a document builds toward it. Each item moved out of a release gets its own line in the plan after that release, so nothing is lost ([chapter 16](16-case-study.md), day four).

## Principles

A principle decides a conflict between two good things, so nobody has to be asked each time. This project has seven. Two of them did real work:

- **Accurate before complete.** A confident wrong answer is worse than none. The author's answer on the knowledge service's speed follows the same order: accuracy comes before speed, an answer may take minutes, and the user always sees that it is still working.
- **One master copy of each fact.** Knowledge lives in Agent E2, and every other copy is generated from it or checked against it. The design choice that applies it, DESIGN-2, serves twelve requirements in four repositories, and the contract check of [chapter 11](11-checks.md) enforces it.

## Division of work

- The person gives the problem, the goals, the users, success and failure, the scope and the reasons.
- The agent writes them down, keeps the person's words where they are clear, asks for a measure where a goal has none, and checks the plan against the scope at the start of each release. In this project that check found 43 requirements for two parts the author expected to stay nearly untouched ([chapter 13](13-working-with-the-agent.md)).

## In VMware terms

This is the part of a design document a VMware architect writes first, with the customer: the business requirements, the scope, and what is out of scope.

## Exercise

Write your product's goal in one sentence that an outsider could check. Add one measure for it, and name one thing the product will not do, with the reason.
