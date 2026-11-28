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

- **The lab sits behind a VPN that only the author's laptop reaches.** The agent's cloud sessions cannot reach it. This one fact shaped the plan: every test that needs the lab sits in one milestone, M8 ([chapter 12](12-slices-and-sessions.md)).
- **The VCF vCommunity Adapter collects every 5 minutes.** No value can be fresher than that, so the limit for a stale value is set in cycles of 5 minutes ([chapter 7](07-requirements-and-acceptance.md)).
- **Neither the adapter nor Agent E2 knows whether a cluster is production in release 1.0.** Agent E2's knowledge keeps two closure levels, one for production and one for other clusters, but release 1.0 applies the production level to every cluster and states the limitation.
- **Model spending stays within US$50 a month once isvara.io is live.** The decision behind it notes that the Vercel subscription already costs US$40. Every design that calls a model is measured against the limit.
- **isvara is a private repository.** The workspace's continuous integration cannot read it without a token, so isvara runs the shared checks in its own pipeline.

One rule in this project shows what a missing reason costs. The project's instructions say: "Stay read-only against VCF Operations and vCenter unless the milestone says otherwise." No reason is written next to it. A session cannot tell from the text whether the rule protects a shared lab, the author's demo, or something else, so it cannot judge an edge case, such as a read that also writes a log entry. One line of reason would settle it.

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
- **About customers.** Agent E2's design orders the ways a security team may approve its web access by what they accept most easily, assuming that "many VCF sites already allow outbound HTTPS to Broadcom for the online depot and patches". The author's field experience can confirm that faster than any test.
- **About users.** The author wrote that a "VMware Admin does not mind 10 seconds waiting as he knows this is not a general chat". The expert's experience is the evidence, and the demo is where it is tested.

## Risks

A risk is written as a cause, an event and an effect, with how likely it is and how much it would hurt. Each one gets a response, an owner, and a trigger or a review date. The four usual responses are to avoid it, reduce it, transfer it to someone better placed, or accept it knowingly.

- **No licence.** The repositories carry no licence file. Without one, ordinary copyright applies, which gives customers no permission to copy the product and change it, against the principle that the product can be forked. Response: accepted for now. Owner: the author, since it is a legal question. Trigger: before the first customer copies the product.
- **The VCF APIs may not expose what the design needs.** Response: reduced, by synthetic data behind the same contract, and by the checks planned for the lab. Owner: the agent. Trigger: the lab milestone, M8.
- **Lab tests wait on the author's time.** Response: reduced, by gathering every lab test into one milestone, so the others can finish without the lab.
- **Cost per visitor may rise.** When isvara.io moves to Agent E2, each call costs less, but Agent E2 holds conversations and reads files and screenshots, so a visitor may cost more. Response: reduced, by the monthly limit above, which the author tracks on the gateway's dashboard.

Most risks are found by the design and the build, after the brief is written ([chapter 8](08-design.md)). The register stays open, and the agent reviews it at the start of each milestone.

## Dependencies

A dependency is anything the work needs that someone else delivers. Writing it down shows who to wait for and what to do meanwhile.

- **Services:** VCF Operations and its Suite API in the lab, Vercel AI Gateway for the model, GitHub Actions for the checks.
- **Other repositories:** a contract's owner changes first and its consumers follow, so pull requests merge in order of ownership: agent-e2, PCM-Adapter, private-cloud-manager, isvara ([chapter 12](12-slices-and-sessions.md)).
- **People:** the author's answers, and the author's laptop for the lab. One answer in this project was "will supply later. remind me". The question stayed open with a trigger: it is asked again when the milestone that needs it starts.
- **Upstream releases:** Agent E2's knowledge follows the current vSphere and VCF releases, so a new Broadcom release is a dependency with work attached.

## Division of work

- The person gives most constraints and their reasons, confirms or corrects assumptions from field experience, and owns risks that only they can act on, such as the licence.
- The agent finds the unstated assumptions in the code, writes every entry with its fields, adds the risks its design creates, and reviews the list at each milestone.
- Both agree on the response to each risk that touches a goal.

## In VMware terms

A VMware design document has the same four sections next to its requirements: constraints, assumptions, risks, and the dependencies of the plan. The customer confirms the assumptions in a design workshop, and each risk carries a mitigation.

## Exercise

List three statements about your project. Sort each into constraint, assumption, risk or dependency, using the tests in the first table. For the assumption, write how and when it will be checked.
