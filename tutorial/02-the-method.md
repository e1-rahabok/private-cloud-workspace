# 2. The method

The method has nine steps. The first seven write the specification, and their files are kept true afterwards. The last two repeat for every piece of work. Each step has a lead: the person who knows the domain and the users, the agent, or both together.

| Step | Question it answers | Led by | Chapter |
|---|---|---|---|
| 1. Map | What exists today? | The agent, corrected by the person | [3](03-map.md) |
| 2. Goals and scope | What must the product achieve, for whom, and what is out? | The person | [4](04-goals-and-scope.md) |
| 3. Interview | What does the agent still need to know? | The agent asks; the person answers | [5](05-the-interview.md) |
| 4. Constraints and risks | What limits the work, what is believed, what could go wrong? | Both | [6](06-constraints-assumptions-risks-dependencies.md) |
| 5. Requirements | What must each part do, and how is it accepted? | Both: the person's input, the agent's draft | [7](07-requirements-and-acceptance.md) |
| 6. Design | How do the parts meet the requirements, and why this way? | The agent | [8](08-design.md), [9](09-seams-and-owners.md) |
| 7. Test plan | How is each requirement proven, where, and with what data? | Both | [10](10-test-plan-and-traceability.md) |
| 8. Checks | Do the parts and the documents still agree after every change? | The agent | [11](11-checks.md) |
| 9. Slices and sessions | In what order is it built, and how does each session run? | The agent, within the person's priorities | [12](12-slices-and-sessions.md), [13](13-working-with-the-agent.md) |

Each slice feeds back into the first steps. A correction or a new answer from the person goes into the map, the brief or a requirement before the next slice starts.

## Input and decisions

The person is the domain expert and the user. The person gives what only they know: the goals, the scope, the users and what they expect, the domain knowledge, the constraints, and the reason behind each. The agent works as the architect. It decides how the product meets the goals, writes each decision where it takes effect, and shows its reasoning, so the person can check it and learn from it.

The author of this project put it this way on 2026-11-28: "Decision is yours, not mine. I give the input and knowledge as I'm the expert and the user." The author went on: "As you're more technical on application development, you design security, scalability, performance, maintainability, etc. Show me so I can learn."

Each decision is written where it takes effect:

- A goal or a line of scope goes into the brief ([chapter 4](04-goals-and-scope.md)).
- A limit the design must accept goes into the constraints, with its reason ([chapter 6](06-constraints-assumptions-risks-dependencies.md)).
- A behaviour goes into a requirement, with its reason beside it ([chapter 7](07-requirements-and-acceptance.md)).
- A choice of how goes into the design, with the options it rejected ([chapter 8](08-design.md)).

## One home for each reason

This project first kept a separate decision log, [DECISIONS.md](https://github.com/e1-rahabok/private-cloud-workspace/blob/8677e71/DECISIONS.md), with 46 entries from WD-001 to WD-046 (WD for "workspace decision"). The workspace retired it on 2026-11-28, for three reasons.

- **It turned answers into rulings.** Each answer the author gave in the interview became a numbered decision, and the agent then carried out the numbered decisions as orders. The answers were knowledge to design with. [Chapter 13](13-working-with-the-agent.md) shows where the habit led.
- **It held a second copy.** An entry restated what the requirements already said, so a change had two places to land.
- **It only grew.** An entry overtaken by a later one stayed, with a pointer: WD-022 says it was "replaced by WD-027", and WD-040 was "renamed by WD-042". A reader had to follow the chain to find what holds now.

One entry shows the second copy. [WD-015](https://github.com/e1-rahabok/private-cloud-workspace/blob/8677e71/DECISIONS.md#wd-015-pcms-live-demo), on PCM's live demo, holds five kinds of statement in one paragraph, and each of them has a better home:

| Part of WD-015 | Kind | Home |
|---|---|---|
| "the L2 workspace only, for performance and capacity management only" | Scope | Brief, SCOPE-5 |
| "says 'No data' when a value is stale" | Requirement | R-LIVE-015, with its reason |
| "never writes to VCF Operations" | Constraint | Brief, SCOPE-5 |
| "reads through with a 60-second cache and stores no metrics" | Design choice | DESIGN-15, with the options rejected |
| "Actions, stories, cases and the calendar are out of 1.0" | Scope | Brief, SCOPE-5 |

An objection came up, and it has an answer. One reason can serve many requirements: WD-001, which makes Agent E2 the source of all domain knowledge, is cited by 12 requirements in four repositories, and copying its reason twelve times would let the copies drift apart. Such a reason gets a home of its own, at the level where it belongs: a principle or a constraint with its own ID, which each requirement cites. The reason is then written once. In this project that reason is PRINCIPLE-5 in the brief, "One master copy of each fact". The design choice that applies it, DESIGN-2, lists the twelve requirements in its Serves line.

The checks change with the method. [tools/spec_check.py](../tools/spec_check.py) fails a requirement whose Source line names no existing question or decision, and 157 of the 202 requirements in the five repositories cited a WD decision. The check exists to hold the method in place, so it moves when the method moves, in the three steps used for any contract ([chapter 9](09-seams-and-owners.md)): accept the new IDs, move each requirement to them, then refuse the old ones. The restructure took all three. The check first accepted the brief's and the design's IDs beside WD-; each repository then moved its requirements to them; and last, the check refused WD-, in the same pull request that deleted the decision log. Every check stayed green on the way.

## The loop back

Building a slice always teaches something: an assumption that was wrong, a meeting point nobody listed, a question only the person can answer. That goes back into the files before the next slice starts, so the files keep pace with the code and grow more accurate with each slice.

## The ideas behind the steps

- The specification is what the people maintain. The code is generated from it and can be generated again. One of the repositories in this project says so in its own decisions: AI writes all of its code, and people maintain the specification.
- Anything that has to outlast a conversation goes into a file in the repository. A conversation is a good place to think something through, but the next session cannot see it.
- When a fact appears in more than one place, one copy is the master, and the others are generated from it or checked against it.
- Every place where two parts depend on each other gets a script that fails when they stop agreeing.
- The person gives input; the agent decides, and writes each decision with its reason where it takes effect.
- Work is built in thin slices, each going end to end across every part it touches, starting with the slice that has the most unknowns.

## Time needed

In this project the first version of the files and two working checks took one long session. The interview and the full set of requirements took another two days, most of it the agent's work, with the author answering questions in the evenings. That is small next to the time the small chats were costing, and the files save that time again at the start of every later session.
