# Intent and principles

Why the product exists, what it must achieve, what it will not do, and the principles that decide a trade-off. Mostly in the author's own words from the interview of 2026-11-26. IDs are explained in the [glossary](glossary.md).

## Origin

The material began as the first edition of the author's book in 2014. Each year it has become deeper, broader and easier to consume, and the reaction has been almost entirely positive. But it lands only when the author explains or demonstrates it, and that does not scale. The software exists so that customers can deploy and use the knowledge without him.

## Goal

- **In the customer's private cloud:** VMware administrators have the author's knowledge inside their own environment, made visible through PCM for every role of the SP5 framework.
- **In public:** isvara.io is recognised worldwide as the authority on large-scale private cloud performance and capacity management, based on VCF.
- **The test of both:** a customer gets value without the author. They install from the manual without contacting him; Agent E2 answers the questions people ask him after his demos; PCM shows each role what he would have pointed at.
- **Horizon:** a few years. Release 1.0 is the first step.

## The parts

| Part | What it is | Who takes it |
|---|---|---|
| Agent E2 | The knowledge, codified: the foundation | Customers, with PCM |
| VCF vCommunity Adapter | Agent E2's KPIs, computed inside VCF Operations | Customers; also installable alone |
| PCM (Private Cloud Manager) | The web app that shows the knowledge for each role | Customers, as a Linux container |
| isvara.io | The public place to learn, ask, practise and contribute | Everyone; never installed or forked |
| Books and spreadsheets | The author's own living editions, updated by hand | Downloaded from isvara.io |

- Customers take all three product repositories, and the parent workspace, as one product ([DECISIONS](../DECISIONS.md), WD-025).
- VCF vCommunity Adapter alone is the simplest deployment: one pak file in VCF Operations, no Linux and no container, with the KPIs, dashboards and reports but without Agent E2. Its documentation presents it as one part of the whole.
- Domain knowledge lives in Agent E2 only. VCF vCommunity Adapter's documentation explains what it computes and how to install it, and points to the knowledge on isvara.io (WD-001).
- The books, spreadsheets and diagrams are a separate, living body of the author's work. They reach isvara.io once or twice a month, and the site refreshes from there weekly.

## Success

- Customers who see the PCM demo find it useful and want to copy it privately, to customise and deploy in their own private cloud (WD-012).
- With PCM, a team becomes proactive: each person ends up with a dashboard that answers exactly their own questions, and a weekly one for deeper analysis (personal dashboards come after 1.0).
- Agent E2 explains a real lab KPI correctly in the live demo.
- isvara.io is where administrators come back to: for tools, for an expert to ask, and to learn.

## Failure

- **Agent E2 fails if it gives confident wrong answers.** Saying "I don't know" is acceptable; an expert says it too.
- **isvara.io fails today** because nothing brings people back regularly, and they cannot tell what has changed.
- **Every requirement can pass and the product still fail** if a customer cannot get value without the author.

## Audience

- **Agent E2 and PCM:** the VMware administrator first. The CIO is not a focus for Agent E2. After L2, the next role in PCM is the tenant or application owner.
- **Customers:** large global enterprises. Their difficulty is organisational, with many teams and many people, which is why PCM is organised by role. Mid-sized companies are not the focus.
- **isvara.io:** VMware administrators and architects who want to master the operation of a private cloud.

## Scope

- **Day 2 only:** running, monitoring, troubleshooting and planning. Design, installation, building, configuration and upgrades (Day 0 and Day 1) are out, because they depend on the release. Agent E2 says so when asked, and points to Broadcom's documentation (WD-026).
- **Release 1.0 in the lab:** a lab demo, with a cloud model through Vercel AI Gateway. The customer's on-premises deployment with a local model comes after release 1.0 (WD-002).
- **PCM replaces VCF Operations narrowly:** performance and capacity management, for the L2 role in the live demo. It does not replace lifecycle, fleet management or SDDC Manager.
- **After 1.0:** personal dashboards in PCM, what-if analysis, the "people" side of operations (convincing application owners), and areas beyond vSphere at depth.

## Principles

These decide a conflict between two good things, without asking the author.

1. **Free.** No paid content, no paid tier.
2. **Accurate before complete.** A confident wrong answer is worse than none. Say what is unknown.
3. **The customer's data stays with the customer.** In the on-premises deployment nothing leaves their network; on isvara.io, visitors remove their own IP addresses and host names before uploading; the site keeps no copy of their files, and keeps their questions and answers for 30 days, to improve the answers (Q-WS-61).
4. **Forkable.** Customers can copy the product privately and make it theirs. Nothing in the product depends at run time on the author's services. Today the repositories have no licence (WD-029), which gives no such permission; it is revisited before the first customer copies the product.
5. **One master copy of each fact.** Knowledge lives in Agent E2; every other copy is generated from it or checked against it (WD-001).
6. **The specification is what people maintain.** AI writes the code; the author and Claude keep the specification true (PCM D-010).
7. **Challenge with evidence.** Few rules hold in operations management. Any assumption, the author's included, can be challenged with evidence (Agent E2's [MISSION.md](https://github.com/e1-rahabok/agent-e2/blob/main/MISSION.md)).

## Measures of authority

- **Search visibility,** from Google Search Console: isvara.io's position for about 20 searches that define the field.
- **Returning visitors and questions asked,** from the site's own counters and question log.
- **Contributions** from the vCommunity, once they open.
- **Referral by Broadcom** is the author's, through marketing.
