# Open questions

Input still needed from the author: a goal, a scope, a requirement, an assumption, a constraint, a reason, or a fact from the field. Design questions are Claude's to decide and never appear here. Each question names the input it needs, and the working assumption Claude follows until the answer comes; the answer is kept word for word in [spec/author-input/](spec/author-input), and its outcome goes into the [brief](spec/brief.md), a requirement or the [system design](spec/design/system.md). IDs are explained in the [glossary](spec/glossary.md).

### Q-WS-137 The key of the 20-second peak of dropped TX packets (settled in M8)

Agent E2's catalog names the VM row "Peak network TX dropped packets" with 20-second limits. The VCF vCommunity Adapter reads `net|droppedTxPct_max`, a 5-minute maximum. VCF Operations lists "Peak Transmitted Packet Dropped within collection cycle" as a 20-second peak metric ([peak-20-second-metrics.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/features/peak-20-second-metrics.md)), but no knowledge file names its key, and the VM key list exported from VCF Operations 9.1.1 has no exact match. Q-WS-81 decided to check it on the lab.

- **Working assumption:** in M2, the adapter's test of R-ADP-008 lists this row as its one known gap, so M2 can finish. In M8, T-ADP-026d reads the lab: if a 20-second key exists, the adapter reads it; if none does, agent-e2's catalog row becomes 5-minute and drops "peak" from its name, then the adapter follows. If you know the key from the field, the answer settles it now.

Answer: that is the key. net|droppedTxPct_max is correct.
