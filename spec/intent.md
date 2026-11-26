# Intent

Why each part exists, for whom, what success looks like, and what is not done. Built from the repositories' own documents and the author's answers in the [interview, round 1](interview-round-1.md). IDs are explained in the [glossary](glossary.md).

## The product

Help large enterprises run their VMware private cloud well, with the knowledge of a senior expert available to every role, through two web apps and one knowledge service.

- **Stage 1 (now):** a demo of PCM in the lab, and the public site isvara.io, both using Agent E2 through a cloud model ([DECISIONS](../DECISIONS.md), W-002).
- **Success for stage 1** ([W-012](../DECISIONS.md), from answers Q-I1 and Q-I2):
  - VMware colleagues and customers who see the PCM demo find it useful and want to fork the repositories privately, to customise and deploy in their own private cloud.
  - In the live demo, Agent E2 explains a real lab KPI correctly.
  - Every contract between the repositories is checked automatically.
- **Not done:** the customer's on-premises deployment with a local model (stage 2).

## PCM (private-cloud-management)

- **For:** operations roles in a large global enterprise: NOC (L1), L2 platform, capacity, and the CIO ([PCM D-005, D-012](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md)).
- **Does:** one workspace per role, each showing only the data that role acts on, with Agent E2 as a team member that explains what the screen shows. Two demos: the synthetic ACME demo for every role, and a live demo of the L2 workspace on the author's lab ([W-015](../DECISIONS.md)).
- **Who sees the demo:** VMware colleagues and customers. Afterwards they should say it is useful and that they want to fork it privately to customise and deploy (Q-I2).
- **Not done (from PCM's decisions):** VCF lifecycle management and security operations (D-008); applications, mainframe and VDI (D-034); end-user help desk and business transactions (D-030); compliance until after release 1.0 (D-022). In the live demo: every role but L2, and everything but performance and capacity management (Q-22, Q-33).

## Agent E2

- **For:** PCM and isvara.io, as their one source of domain knowledge ([W-001](../DECISIONS.md)).
- **Does:** answers like a senior VMware performance and capacity expert: the facts, the mechanism, the evidence and what to check next; the fix stays the human's decision ([MISSION.md](https://github.com/e1-rahabok/agent-e2/blob/main/MISSION.md)). Holds a conversation over several turns, and reads CSV files and VMware screenshots (Q-I1).
- **Success for stage 1** ([W-013](../DECISIONS.md), from answers Q-I3, Q-5, Q-7): its free-text answers pass an automated grader with a strong model as judge, on Gemma 4 31B or a later version. Accuracy comes before speed: an answer may take minutes, and the user always sees that it is still working.
- **Not done:** the final fix in troubleshooting. Fine-tuning the model is not planned; the reasons, with the pros and cons, are in [design/fine-tuning.md](design/fine-tuning.md).

## PCM-Adapter

- **For:** VCF Operations administrators, and PCM, which reads what it publishes.
- **Does:** computes the KPIs that Agent E2 defines, and publishes them on the vCenter objects in VCF Operations.
- **May change:** anything, including its identity in VCF Operations (Q-I4, Q-2; [W-016](../DECISIONS.md)).
- **Not done:** its own definitions. Every limit, band and rule comes from Agent E2's catalog (Q-15).

## isvara.io

- **For:** VMware administrators and architects learning to run a private cloud (Q-I5).
- **Does:** serves the reasons visitors come ([W-022](../DECISIONS.md)): read articles, books and infographics; ask Agent E2; listen to a podcast; solve with calculators; catch up on what changed; fork the base; find with search; practise with a quiz; engage through a survey; download the books. Connects to no live system ([W-004](../DECISIONS.md)). Holds no knowledge of its own (Q-18).
- **Success** (Q-I5): every knowledge file becomes a page a person can read and bookmark; a reader always knows where they are in the whole; the knowledge can be explored in several ways; Agent E2 answers with sources a reader can open; the exam exists.
- **Not done:** live connections, sign-in, paid content.
- **Plan:** each feature, before and after, waits for the author's review in [design/isvara-revamp.md](design/isvara-revamp.md).
