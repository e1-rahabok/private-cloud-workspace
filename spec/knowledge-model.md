# Knowledge model

How the knowledge is organised for people and checked for completeness. It is shared by Agent E2 (what it holds), isvara.io (how people find and learn it) and the knowledge factory (where help is needed). Agent E2 owns the knowledge itself ([DECISIONS](../DECISIONS.md), WD-001); this file is the model the three use. IDs are explained in the [glossary](glossary.md).

## Scope: Day 2

The knowledge covers running an existing private cloud: monitoring, troubleshooting and planning. Design, installation, building, configuration and upgrades are out, because they change with each release (WD-026). Settings stay in only where they affect performance, capacity or availability, as Agent E2's `what-to-set` files already do.

## Three learning paths

The paths are how a reader looks for knowledge, and the backbone of isvara.io.

| Path | Topics | Agent E2 tag |
|---|---|---|
| Architecture | CPU, memory, storage, network | `technology` |
| IT management | SP5's five pillars: availability, performance, security, capacity, value; with monitoring, troubleshooting | `pillar` |
| Product | vSphere, vSAN, NSX, VCF Operations, Kubernetes, Windows, Linux, by object type | `product`, `object` |

- The glossary (`term-meaning`) serves search and sits under no lens.
- The paths overlap on purpose. CPU, performance and the cluster meet in the cluster's CPU contention; a reader can arrive by any of the three and move to the others from there.
- Every path is generated from the tags each knowledge file already carries, so isvara.io holds no structure of its own.
- Configuration and inventory are not pillars: they sit under all five ([SP5 overview](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/overview.md), section The five pillars). A `what-to-set` file appears under the pillars its `pillar` tag names.

## Four lenses: the completeness check

Each topic is known through four lenses. A reader, or Agent E2, can be strong in one and weak in the next, about the same component. The lenses are not navigation; they check that a topic is complete and tell a reader what they are missing.

| Lens | The question it answers | Agent E2 today |
|---|---|---|
| How it works | What happens inside the technology | `how-it-works` files |
| How it is measured | What a counter counts: where, how often, with which statistic | `metric-meaning` files, the catalog |
| How it is managed | The discipline: KPIs, class of service, capacity and performance practice | The SP5 framework, `what-to-set`, `health-check` and `decision-tree` files |
| How it fails | Diagnosis, often across several areas and systems | 12 `troubleshooting` flows, mostly within one area |

Examples from the field:

- **Measured, without how it works.** The Guest OS shows memory 90% used and the administrator adds RAM. Most of it was file cache, which the hypervisor sees as inactive.
- **How it works, without how it is measured.** An engineer who knows the CPU scheduler well reads a weekly chart as showing the peak. A one-week rollup averages away the 20-second spikes.
- **Knows the metric, not the difference.** A practitioner who knows how ESXi works does not know the difference between CPU Usage and CPU Used.
- **Managed, without context.** "CPU Ready above 5% is bad" is applied to every VM. On Bronze it may be within the promise; on Gold it may break it.
- **One pillar, not the next.** A capacity planner sizes by vCPU-to-core ratio and never looks at contention; a performance specialist answers every problem with "add hosts".
- **Each team in its own layer.** The array shows 2 ms, the VM 40 ms of disk latency, the Guest OS a long queue. Each is right about its layer; nobody follows the I/O path from application to array.
- **Across the virtual and physical network.** The physical switch shows no drops; the VM drops packets at its virtual NIC.
- **Kubernetes across layers.** A pod is slow and kubectl shows nothing, because the contention is in the VM below the node.

## Depth

Each topic, in each lens, runs from Level 100 (name it) to Level 400 (explain the mechanism, know when the reading misleads, combine facts to a conclusion). The levels are Agent E2's ([KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md), section Misconceptions and Level 400). The knowledge base is written at Level 400 and assumes 100 and 200.

## Experience: the deepest gap

What separates the author from a strong Level 400 reader is experience: long-chain troubleshooting and pattern recognition. Two forms would let Agent E2 hold some of it. Both are proposals for agent-e2, which owns the knowledge, and come after release 1.0 ([WD-035](../DECISIONS.md)):

- **Workload footprints.** For each recurring pattern (backup window, antivirus scan, patching night, batch job, boot storm), its shape across metrics, objects and time. Backup and antivirus leave different footprints, so a footprint tells them apart.
- **Investigations over several steps.** A flow that crosses areas and goes back in time: trace the symptom to the layer below, look wider (other objects) or deeper (finer metrics, longer history), check what changed. In PCM, Agent E2 can ask for more data; on isvara.io, it asks the visitor for another screenshot or CSV file.

## Scale

At large scale, some answers change: thousands of VMs, many vCenters and regions. Instead of tagging every file, an "At large scale" note is added where the answer changes. The notes come after release 1.0 ([WD-035](../DECISIONS.md)):

- performance: start from the cluster KPI's worst VM and its 90th percentile, because nobody can look at 10,000 VMs;
- alerts: per-VM alerts become storms, so insights and the daily check replace most of them;
- dashboards: top-N lists, distributions and heat maps replace tables of VMs;
- capacity: many clusters, classes of service, regions, procurement lead time;
- statistics: an average across thousands of objects hides everything; percentiles and worst-of carry the meaning;
- collection: metric volume and collection interval have a real cost.

Once the notes exist, the isvara.io reader says once whether their estate is small or large, and the notes for their estate are shown first.

## Areas and coverage

| Area | Coverage today |
|---|---|
| vSphere: ESXi, VM, cluster, resource pool, datastore, distributed switch | Deep: about 200 files |
| VCF Operations | Partial: 10 files |
| Guest OS: Windows, Linux | Partial: 16 files |
| vSAN, NSX, Kubernetes (VKS), physical servers, switches and arrays | Little or none |
| Workloads: backup, antivirus, databases, VDI | None, beyond mentions |

Breadth grows through contributions at isvara.io (WD-024): the coverage table, by area and lens, shows the vCommunity exactly where help is needed.

## Uses

- **Agent E2:** the lenses check each topic for completeness; the paths match its tags; the experience forms are its next step.
- **isvara.io:** the paths are the navigation; the lenses drive the quiz's diagnosis ("strong in how CPU works, weak in how it is measured"); the coverage table invites contributions.
- **PCM:** the lenses explain why the L2 workspace shows the same object from several angles: the KPI (managed), its parts (measured) and the troubleshooting flow (fails).

## Proposals for agent-e2

To raise in agent-e2's own question file, since agent-e2 owns the knowledge design:

1. Add the knowledge model to [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md): the paths, the lenses as a completeness check, the Day 2 boundary.
2. After release 1.0 ([WD-035](../DECISIONS.md)): add workload footprints and investigations over several steps as knowledge forms.
3. After release 1.0 ([WD-035](../DECISIONS.md)): add "At large scale" notes where the answer changes.
