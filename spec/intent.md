# Intent

Why each part exists, for whom, what success looks like, and what is not done. **Draft:** taken from the repositories' own documents; the lines marked *(interview)* wait for the author's answers in [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md), section Intent.

## The product

Help large enterprises run their VMware private cloud well, with the knowledge of a senior expert available to every role, through two web apps and one knowledge service.

- **Stage 1 (now):** a demo of PCM in the lab, and the public site isvara.io, both using Agent E2 through a cloud model ([DECISIONS](../DECISIONS.md), W-002).
- **Success for stage 1:** *(interview, Q-I1)*
- **Not done:** the customer's on-premises deployment with a local model (stage 2).

## PCM (private-cloud-manager)

- **For:** operations roles in a large global enterprise: NOC (L1), L2 platform, capacity, and the CIO ([PCM D-005, D-012](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md)).
- **Does:** one workspace per role, each showing only the data that role acts on, with Agent E2 as a team member that explains what the screen shows.
- **Who sees the demo, and what they must believe after it:** *(interview, Q-I2)*
- **Not done (from PCM's decisions):** VCF lifecycle management and security operations (D-008); applications, mainframe and VDI (D-034); end-user help desk and business transactions (D-030); compliance until after release 1.0 (D-022).

## Agent E2

- **For:** PCM and isvara.io, as their one source of domain knowledge ([W-001](../DECISIONS.md)).
- **Does:** answers like a senior VMware performance and capacity expert: the facts, the mechanism, the evidence and what to check next; the fix stays the human's decision ([MISSION.md](https://github.com/e1-rahabok/agent-e2/blob/main/MISSION.md)).
- **Success for stage 1:** *(interview, Q-I3)*
- **Not done:** fine-tuning a model; the final fix in troubleshooting. [e1: why do we need to fine tune a model? Document the pros and cons on a separate design document as it seems to be a major design work. Provide recommendation]

## PCM-Adapter

- **For:** VCF Operations administrators, and PCM, which reads what it publishes.
- **Does:** computes the KPIs that Agent E2 defines, and publishes them on the vCenter objects in VCF Operations.
- **Not done:** *(interview, Q-I4)*

## isvara.io

- **For:** *(interview, Q-I5)*
- **Does:** lets people learn how to run a private cloud: reading, tools, a game and an exam, with Agent E2 answering questions. Connects to no live system ([W-004](../DECISIONS.md)).
- **Success:** *(interview, Q-I5)*
- **Not done:** *(interview, Q-I5)*
