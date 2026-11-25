# Open questions

Questions for the author that block or shape a milestone. One entry each, with a recommendation. When answered, the answer moves to [DECISIONS.md](DECISIONS.md) or to the right repository's log, and the entry is deleted.

## Q-1 VM and Guest OS sub-metric names (blocks M1)

PCM-Adapter publishes 11 VM Performance and Guest OS Performance sub-metrics under names other than the Agent E2 catalog's. The limits and excluded-when-green agree; only the names differ. Cluster Performance, ESXi Performance, Cluster Risk and Cluster Consumption already use catalog names, through each module's `LABELS` table.

| KPI | Adapter | Agent E2 catalog |
|---|---|---|
| VM Performance | CPU Co-Stop | Peak CPU Co-stop among any vCPU |
| VM Performance | CPU Ready | Peak CPU Ready among any vCPU |
| VM Performance | CPU Overlap | Peak CPU Overlap |
| VM Performance | Disk Latency | Peak read/write latency among vDisks |
| VM Performance | Network Dropped Tx | Peak network TX dropped packets |
| VM Performance | CPU Run | CPU Net Run |
| VM Performance | Memory Ballooned | VM Memory Ballooned |
| Guest OS Performance | Guest CPU Run Queue per vCPU | Peak vCPU run queue length |
| Guest OS Performance | Guest Disk Queue | Peak disk queue length |
| Guest OS Performance | Guest Free Memory | Free memory |
| Guest OS Performance | Guest Page-Out Rate | Memory page-out rate |

- **Recommendation:** add the catalog names to the adapter's `LABELS`, as the cluster modules do. First check what a label changes in VCF Operations (the metric key, or only the display name), because a key change breaks dashboards and history.
- **Needs your field knowledge:** "Guest CPU Run Queue per vCPU" and "Peak vCPU run queue length" may not be the same measure: per vCPU against a total. Which is right?

## Q-2 The `vCommunity|` key prefix

The repository is now PCM-Adapter. The metric keys still start with `vCommunity|`, and the pack is still named vCommunity in VCF Operations.

- **Recommendation:** keep the keys. Renaming them breaks every dashboard, view, alert and super metric that uses them, and the history of every metric on every object. Rename only the display name of the pack, if at all.

## Q-3 Renaming references in the child repositories (M1)

The old repository name appears in agent-e2 (10 files, including knowledge files and `harness/expert_agent.py`), PCM-Adapter (12 files) and private-cloud-management (3 files). GitHub redirects the old URLs, so nothing is broken today.

- **Recommendation:** one pull request per repository in M1, leaving archive files as they are.

## Q-4 Where the public Agent E2 runs (blocks M5)

isvara.io is a Next.js app on Vercel. Agent E2 is a Python HTTP service with its knowledge base on disk. PCM's Agent E2 runs on the lab VM, which the Internet cannot reach and should not.

- **Options:** (a) Agent E2 as a Vercel Python function in its own project; (b) a small public container host; (c) a static export of the knowledge base inside isvara, with isvara calling the model itself (this repeats Agent E2's logic in TypeScript, so it breaks W-001).
- **Recommendation:** decide after M4, with the cost per question and the start-up time of (a) measured.
