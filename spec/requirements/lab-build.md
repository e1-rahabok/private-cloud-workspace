# Requirements: lab build

An automatic build of nested virtual ESXi hosts with memory tiering in the author's lab, in the new repository [lab-build](https://github.com/e1-rahabok/lab-build) (empty today). The physical lab hosts have no memory tiering, so the tiering parts of Cluster Risk and Cluster Consumption cannot be tested without it (answer to Q-WS-38 in the [interview, round 1](../interview-round-1.md); [WD-018](../../DECISIONS.md)). It is built after release 1.0 ([WD-031](../../DECISIONS.md)).

### R-LAB-001 One command builds the tiered nested hosts

Milestone: after release 1.0 ([WD-031](../../DECISIONS.md)).

Source: answer to Q-WS-38.

- Given the lab vCenter (https://10.115.1.87) and the author's credential file in `$HOME\.secrets\`
- When the build command runs on the author's laptop
- Then it creates nested ESXi hosts with a virtual NVMe device configured as the memory tier
- And adds them to one cluster of their own
- And reports each host's DRAM size and NVMe tier size

Test scenarios:
- T-LAB-001a (lab, automated by the build's own verify step, to write): after the build, each nested host reports a memory tier size above 0 through the vSphere API.

### R-LAB-002 The tiered cluster is monitored by the lab VCF Operations

Milestone: after release 1.0 ([WD-031](../../DECISIONS.md)).

Source: answer to Q-WS-38; WD-018.

- Given the nested cluster is built
- When one collection cycle of the VCF vCommunity Adapter has passed
- Then the cluster carries data for the tiering parts: Worst ESXi active memory (tiered hosts), Worst ESXi NVMe read latency, Cluster-wide ESXi DRAM Consumed and Cluster memory tiering consumption

Test scenarios:
- T-LAB-002a (lab, automated by PCM-Adapter's tools/validate, to extend): the four tiering keys have a sample newer than one cycle on the nested cluster.

### R-LAB-003 The build can be repeated and removed

Milestone: after release 1.0 ([WD-031](../../DECISIONS.md)).

Source: answer to Q-WS-38 ("automatic build").

- Given the build has run once
- When it runs again
- Then it changes nothing that already matches
- And a separate remove command deletes everything the build created, and nothing else

Test scenarios:
- T-LAB-003a (lab, automated, to write): run the build twice; the second run reports no change. Run remove; vCenter shows none of the build's objects.

### R-LAB-004 No secret in the repository

Milestone: after release 1.0 ([WD-031](../../DECISIONS.md)).

Source: WD-011.

- Given the build's scripts
- When they need a password
- Then they read it from a DPAPI file in `$HOME\.secrets\` and never print, log or commit it

Test scenarios:
- T-LAB-004a (anywhere, automated by a secret scan in the repository's CI, to write): no password, token or key appears in the repository.

## Questions for round two

The questions on this file, with their decisions, are in the [interview, round 2](../interview-round-2.md): Q-WS-119 to Q-WS-122. None is open.
