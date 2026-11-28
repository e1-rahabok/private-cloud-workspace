# Open questions

Questions only the author can answer. Everything else from the interview is decided; the records are [round 1](spec/interview-round-1.md), [round 2](spec/interview-round-2.md), [round 3](spec/interview-round-3.md), [round 4](spec/interview-round-4.md), [round 5](spec/interview-round-5.md) and [round 6](spec/interview-round-6.md). IDs are explained in the [glossary](spec/glossary.md).

### Q-WS-137 The key of the 20-second peak of dropped TX packets (settled in M8)

Agent E2's catalog names the VM row "Peak network TX dropped packets" with 20-second limits. The VCF vCommunity Adapter reads `net|droppedTxPct_max`, a 5-minute maximum. VCF Operations lists "Peak Transmitted Packet Dropped within collection cycle" as a 20-second peak metric ([peak-20-second-metrics.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/features/peak-20-second-metrics.md)), but no knowledge file names its key, and the VM key list exported from VCF Operations 9.1.1 has no exact match. Q-WS-81 decided to check it on the lab.

- **Recommendation:** in M2, the adapter's test of R-ADP-008 lists this row as its one known gap, so M2 can finish. In M8, T-ADP-026d reads the lab: if a 20-second key exists, the adapter reads it; if none does, agent-e2's catalog row becomes 5-minute and drops "peak" from its name, then the adapter follows. If you know the key from the field, the answer settles it now.

Answer:
