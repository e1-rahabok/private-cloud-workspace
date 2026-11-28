# Interview, round 5

Questions in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md) answered by the author on 2026-11-27, with the answers as written and what follows from each. IDs are explained in the [glossary](../glossary.md).

## Q-WS-120 Where the nested ESXi hosts run

**Answer:** "in the lab. This is after Release 1.0"

**Result:** the nested hosts run in the author's lab. The cluster, datastore, network and spare capacity are asked when the lab build starts, after release 1.0 ([DECISIONS](../../DECISIONS.md), WD-031; [ROADMAP](../../ROADMAP.md), section After release 1.0).

## Q-WS-122 Licences for the nested hosts

**Answer:** "Yes."

**Result:** the lab licences cover two more ESXi hosts. Nothing more is needed for the lab build.

## Q-WS-135 The upstream licence of the VCF vCommunity Adapter

**Answer:** "settled already. Close this"

**Result:** the question is closed. No file in the five repositories records how it was settled, and the [PCM-Adapter](https://github.com/e1-rahabok/PCM-Adapter) repository still has no LICENSE file.
