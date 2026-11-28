# 6. Constraints, assumptions, risks and dependencies

## Four kinds of condition

Requirements say what the product must do. Four other kinds of statement describe the conditions the work happens under. They are easy to confuse, and each one is handled differently.

| Kind | Meaning | Test of the kind |
|---|---|---|
| Constraint | A limit the design must accept, set from outside it | Can the design change it? No. |
| Assumption | Something believed true and not yet verified | Has anyone checked it? Not yet. |
| Risk | An uncertain event that would hurt a goal | Could it happen, and would it matter? |
| Dependency | Something the work needs from outside it | Who else has to deliver? |

The difference matters because each kind gets a different treatment. A constraint is designed around. An assumption is verified, and until then the design limits the damage if it is false. A risk gets a response and an owner. A dependency gets a date or a trigger.

In this project all four live in the brief, [spec/brief.md](../spec/brief.md), with IDs such as CONSTRAINT-1, ASSUMPTION-1, RISK-1 and DEPENDENCY-1, so a requirement or a design choice can cite the one it rests on.

## Constraints

A constraint comes from the platform, the budget, the law, the environment, or the person's own policy. It needs its reason, because a constraint without one is either obeyed blindly or quietly worked around. Constraints from this project:

- **The lab sits behind a VPN that only the author's laptop reaches** (CONSTRAINT-6). The agent's cloud sessions cannot reach it. This one fact shaped the plan: every test that needs the lab sits in one milestone, M8 ([chapter 12](12-slices-and-sessions.md)).
- **The VCF vCommunity Adapter collects every 5 minutes.** No value can be fresher than that, so the limit for a stale value is set in cycles of 5 minutes ([chapter 7](07-requirements-and-acceptance.md)).
- **Neither the adapter nor Agent E2 knows whether a cluster is production in release 1.0** (CONSTRAINT-5). No data source in the lab holds it. Agent E2's knowledge keeps two closure levels, one for production and one for other clusters, so the design applies the production level to every cluster and states the limitation (DESIGN-18).
- **Gateway spending stays within US$50 a month once isvara.io is live** (CONSTRAINT-1). The Vercel subscription of US$40 is apart, and a benchmark run has its own budget of US$100. Every design that calls a model is measured against these limits. A limit checked only before a run is a forecast. In November 2026 the US$100 was checked against a projection before each benchmark round, and three rounds in one week spent about US$350, because nothing counted the money while a round ran or limited how often one ran. The constraint now counts each run on the money it spends, never runs the full round, and reuses answers whose inputs have not changed (DESIGN-31).
- **isvara is a private repository.** The workspace's continuous integration cannot read it without a token, so isvara runs the shared checks in its own pipeline.

One rule in this project shows what a missing reason costs. The project's instructions say: "Stay read-only against VCF Operations and vCenter unless the milestone says otherwise." No reason was written next to it. A session could not tell from the text whether the rule protects a shared lab, the author's demo or something else, so it could not judge an edge case, such as a read that also writes a log entry. The brief now holds the rule inside CONSTRAINT-6, with its reason: "it is the author's own lab and network".

## Assumptions

An assumption that turns out false costs the most when it is found late, after the design is approved and the build is under way. Each one is written with:

- the statement;
- why it is believed, and on whose evidence;
- what breaks if it is false;
- how and when it will be checked;
- its status: unconfirmed, confirmed or false.

The PCM core design names its biggest risk as an assumption: several designs depend on data "whose API support has not been verified", such as 20-second peak metrics and log queries ([pcm-core.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/pcm/core/design-notes/pcm-core.md), section 4). Each one is marked "to verify on the live system". The design then limits the damage: the prototype runs on synthetic data behind the same API contract the live data will use, "so nothing built now depends on the answer". That is the professional handling of an assumption: write it down, plan when it is checked, and arrange the design so that a false answer changes one layer.

Assumptions hide in other places too:

- **In the code.** The interview found that the demo data holds 13 months of history while the lab holds a few days. Nothing stated it; the charts simply relied on it ([chapter 5](05-the-interview.md)).
- **Inside a requirement.** The adapter's requirement on a read-only account says: "Verify on the lab that the read-only account can read adapters, solutions and resources." It is an assumption, marked so that the lab session tests it.
- **About customers.** Agent E2's design orders the ways a security team may approve its web access by what they accept most easily, on this assumption: "Many VCF sites already allow outbound HTTPS to Broadcom for the online depot and patches". The author's field experience can confirm that faster than any test.
- **About users.** ASSUMPTION-2 says a 10-second wait between progress reads is acceptable. Its status is confirmed, by the author's words: "VMware Admin does not mind 10 seconds waiting as he knows this is not a general chat." The expert's experience is the evidence, and the demo is where it is tested.
- **About cost.** ASSUMPTION-4 says Agent E2 may cost more per visitor than isvara.io's current assistant: its model costs less per call, but it holds conversations and reads CSV files and screenshots. Status: unconfirmed. Check: the cost per answer, measured in M5.

## Risks

A risk is written as a cause, an event and an effect, with how likely it is and how much it would hurt. Each one gets a response, an owner, and a trigger or a review date. The four usual responses are to avoid it, reduce it, transfer it to someone better placed, or accept it knowingly.

The brief keeps a shorter form: each risk names its effect, what reduces it, and who acts. Four from this project:

- **RISK-1 Agent E2 gives confident wrong answers.** An earlier generation was confidently wrong on 31 to 41% of open answers. Reduced by: a graded answer set on every change of model or prompt, sources on every answer, and the Day 2 scope. Acts: the agent.
- **RISK-2 No licence gives no right to copy.** The repositories carry no licence file, by the author's choice (CONSTRAINT-4). Without one, GitHub's terms let others view and fork a public repository on GitHub, but give no permission to copy it elsewhere, change it or run it, against the principle that the product can be forked. Reduced by: a licence chosen before the first customer copies the product. Acts: the author, since it is a legal question.
- **RISK-3 Lab work waits on one laptop.** Reduced by: all lab work in M8, fakes for everything else, and a list of the lab checks each earlier pull request could not run. Acts: the agent prepares, the author runs the session.
- **RISK-4 Gateway spending exceeds the budget.** Reduced by: a daily ceiling on model calls, limits per visitor and a budget per benchmark run, which the design builds in (DESIGN-20). Acts: the agent builds the limits; the author watches the gateway's dashboard.

Most risks are found by the design and the build, after the brief is written ([chapter 8](08-design.md)). The agent keeps the list open and reviews it at the start of each milestone; the person adds what the field has taught.

## Dependencies

A dependency is anything the work needs that someone else delivers. Writing it down shows who to wait for and what to do meanwhile.

- **Services** (DEPENDENCY-9): VCF Operations and vCenter in the lab, Vercel for hosting and the model gateway, GitHub Actions for the checks, and Broadcom's documentation. Each entry names who provides it and which milestone needs it.
- **Other repositories:** a contract's owner changes first and its consumers follow, so pull requests merge in order of ownership: agent-e2, PCM-Adapter, private-cloud-manager, isvara ([chapter 12](12-slices-and-sessions.md)).
- **People:** the author's answers, the approval of each milestone (DEPENDENCY-1), and a lab session with the author's laptop (DEPENDENCY-7). One answer in this project was "will supply later. remind me". The question stayed open with a trigger: it is asked again when the milestone that needs it starts.
- **Upstream releases:** Agent E2's knowledge follows the current vSphere and VCF releases, so a new Broadcom release is a dependency with work attached.

## Division of work

- The person gives most constraints and their reasons, confirms or corrects assumptions from field experience, and owns risks that only they can act on, such as the licence.
- The agent finds the unstated assumptions in the code, writes every entry with its fields, adds the risks its design creates, and reviews the list at each milestone.
- Both agree on the response to each risk that touches a goal.

## In VMware terms

A VMware design document has the same four sections next to its requirements: constraints, assumptions, risks, and the dependencies of the plan. The customer confirms the assumptions in a design workshop, and each risk carries a mitigation.

## Exercise

List three statements about your project. Sort each into constraint, assumption, risk or dependency, using the tests in the first table. For the assumption, write how and when it will be checked.
