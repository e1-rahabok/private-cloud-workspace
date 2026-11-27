# Open questions

Questions only the author can answer. Everything else from the interview is decided; the records are [round 1](spec/interview-round-1.md), [round 2](spec/interview-round-2.md), [round 3](spec/interview-round-3.md) and [round 4](spec/interview-round-4.md). IDs are explained in the [glossary](spec/glossary.md).

## Q-120 Where the nested ESXi hosts run

The lab build creates two small nested ESXi hosts with memory tiering ([lab-build requirements](spec/requirements/lab-build.md)). Needed when the lab build starts, after release 1.0 ([WD-031](DECISIONS.md)); the author will supply it then.

- **Needs you:** the physical cluster, datastore and network to use, and how much CPU, memory and NVMe space you can spare.

**Answer:**

## Q-122 Licences for the nested hosts

Needed with Q-120.

- **Needs you:** do the lab licences cover two more ESXi hosts?

**Answer:**

## Q-135 The upstream licence of the VCF vCommunity Adapter

The [PCM-Adapter](https://github.com/e1-rahabok/PCM-Adapter) repository is a fork of [vmbro/VCF-Operations-vCommunity](https://github.com/vmbro/VCF-Operations-vCommunity).

- **What the upstream repository holds:** a LICENSE file with the PolyForm Noncommercial License 1.0.0 and a "Required Notice" naming Onur Yuzseven.
- **What the fork did:** removed that file in commit `3be3fe2` ("Remove LICENSE file").
- **Which files are upstream code:** 31 of the 32 files with "Author: Onur Yuzseven" in their header also exist upstream.
- **Why it matters:**
  - PolyForm Noncommercial asks that anyone who passes on the software includes the licence terms and the Required Notice.
  - It allows noncommercial use only. Customers that are companies copying the product (WD-025) would be commercial use.
  - [WD-029](DECISIONS.md) records "no licence file" for the author's own repositories. It does not cover code under another author's licence.
- **Recommendation:** restore the upstream LICENSE file and its Required Notice in the PCM-Adapter repository now. Before the first customer copies the product, ask Onur Yuzseven for permission for commercial use, or replace the upstream code. This is not legal advice.

**Answer:**
