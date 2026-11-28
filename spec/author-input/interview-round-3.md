# Interview, round 3

The last questions only the author could answer, asked in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md) on 2026-11-26, with his answers as written and what follows from each. IDs are explained in the [glossary](../glossary.md).

## Q-WS-60 The product's name

**Answer:** "Manager, not Management."

**Result:** the product is Private Cloud Manager, PCM for short ([DECISIONS](../../DECISIONS.md), WD-028). The books keep "Private Cloud Management" as the name of the discipline.

## Q-WS-88 Guest OS run queue: per vCPU, or total

**Answer:** "the one in VCF Operations is per vCPU. The real source in Windows or Linux, I'm unsure."

**Result:** Agent E2's knowledge base already settles the source ([run-queue.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/cpu/metrics/run-queue.md)): Windows and Linux report one queue for the whole Guest OS (Windows leaves out running threads; Linux counts them), and VCF Operations divides it by the VM's vCPU count. The limits (0, 2, 4, 8, 16) apply per vCPU, so the adapter's name is the precise one. Agent E2's catalog row is renamed "Peak run queue length per vCPU" in M2, and PCM-Adapter's label follows it (Q-WS-1: names come from Agent E2).

## Q-WS-120 and Q-WS-122 Lab placement and licences

**Answer:** "will supply later. remind me."

**Result:** both stay in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md). They are needed when the lab build starts, after release 1.0 (WD-031). Answered in [round 5](interview-round-5.md).

## Q-WS-130 Events for birds-of-a-feather sessions

**Answer:** "not sure what you mean here. We have VMUG event."

**Result:** a birds-of-a-feather session is an informal discussion at an event, among people who share an interest; the author's visitor model listed requests for them. The contribution form on isvara.io offers "Request a session at a VMUG event", with a topic and a free line for the city or event.

## Q-WS-132 A GitHub organization

**Answer:** "not applicable. This is my personal project."

**Result:** the repositories stay under the author's account. Customers copy them from there by mirroring (WD-025).

## Q-WS-133 The licence

**Answer:** "leave it blank as it uses GitHub default."

**Result:** no licence file for now (WD-029). None of the five repositories has one today. The consequence is recorded with the decision, to be revisited before the first customer copies the product.
