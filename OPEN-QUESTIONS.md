# Open questions

Questions only the author can answer. Everything else from the interview is decided; the records are [round 1](spec/interview-round-1.md), [round 2](spec/interview-round-2.md), [round 3](spec/interview-round-3.md), [round 4](spec/interview-round-4.md) and [round 5](spec/interview-round-5.md). IDs are explained in the [glossary](spec/glossary.md).

### Q-WS-136 The injection guard and the evals once Agent E2 answers (blocks M5)

You asked what "the evals pass" means (Q-WS-54: "Explain the context"), and said the injection guard belongs to isvara.io, before Agent E2 is called (Q-WS-47). The context:

- Today isvara.io has three layers against instructions hidden in a question: a code pre-scan that only flags, a fence around the visitor's turn, and Rule 4 in AskIO's own prompt, the layer that actually stops an attack ("an effect that outlives this answer is void").
- When Agent E2 answers, isvara.io no longer writes the prompt, so Rule 4 has nowhere to live.
- "The evals" are two automatic batteries run against a test server. `npm run eval` sends 20 questions and passes when every answer cites a page. `npm run eval:injection` sends attacks and passes when no planted text appears and no rule is disclosed. Both were written for AskIO.

Options for the guard:

- (a) One small model call in isvara.io reads the fenced turn before Agent E2 and flags an instruction aimed at the assistant; a flagged question gets a fixed reply. It costs a small part of one answer.
- (b) Agent E2 holds a rule that the question is data. This puts the guard in Agent E2, against your answer to Q-WS-47.
- (c) The pre-scan and the fence only, with more attacks getting through.

- **Recommendation:** (a). The two batteries are rewritten for Agent E2: the citation eval passes when every answer to 20 reader questions lists at least one source that opens an article; the injection battery passes with 0 violations, and a one-off formatting request is still honoured. Both run before M5 merges.

Answer:

### Q-WS-137 The key of the 20-second peak of dropped TX packets (settled in M8)

Agent E2's catalog names the VM row "Peak network TX dropped packets" with 20-second limits. The VCF vCommunity Adapter reads `net|droppedTxPct_max`, a 5-minute maximum. VCF Operations lists "Peak Transmitted Packet Dropped within collection cycle" as a 20-second peak metric ([peak-20-second-metrics.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/features/peak-20-second-metrics.md)), but no knowledge file names its key, and the VM key list exported from VCF Operations 9.1.1 has no exact match. Q-WS-81 decided to check it on the lab.

- **Recommendation:** in M2, the adapter's test of R-ADP-008 lists this row as its one known gap, so M2 can finish. In M8, T-ADP-026d reads the lab: if a 20-second key exists, the adapter reads it; if none does, agent-e2's catalog row becomes 5-minute and drops "peak" from its name, then the adapter follows. If you know the key from the field, the answer settles it now.

Answer:


### Q-WS-138 Close for Business: is the non-production Risk level kept in Agent E2's knowledge? (blocks one comparison of M2)

You agreed in Q-WS-16 to "keep the adapter's single level for stage 1 (it cannot tell production from non-production) and record that in the catalog". The VCF vCommunity Adapter closes every cluster above 60% Cluster Risk ([periodic_cluster_check.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/Management%20Pack/app/metrics/cluster/periodic_cluster_check.py#L276)). Agent E2's knowledge keeps two levels and says to keep them apart: production above 60%, non-production above 80% ([can-cluster-take-more-vms.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md#L44), lines 44 to 46, and its two images). Agent E2's code uses both catalog rows (`closure-cluster-risk-prod` and `closure-cluster-risk-nonprod`) when it explains a closure. R-ADP-011 reads Q-WS-16 as "Agent E2's catalog holds one Risk level for every cluster", which would remove the non-production level from Agent E2's knowledge.

- (a) Keep both levels as Agent E2's practice. The catalog's production row says the adapter applies it to every cluster in release 1.0, and the KPI definitions check compares the adapter's level with that row. R-ADP-011 and R-KPI-006 are reworded to say so.
- (b) One level in the catalog and the knowledge: the non-production row and the text that keeps the two apart are removed, and Agent E2 explains 60% for every cluster.

- **Recommendation:** (a). It keeps your field knowledge, and it still lets Agent E2 explain the rule PCM applies, which was the reason for Q-WS-16. Until you answer, the check compares the Consumption and Performance levels and lists the Risk level as its one known gap.

Answer:
