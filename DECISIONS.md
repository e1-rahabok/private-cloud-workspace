# Decisions

Decisions that bind more than one repository. A decision inside one repository goes in that repository's own log:

| Repository | Its decision log |
|---|---|
| agent-e2 | [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) |
| PCM-Adapter | Its issues and pull requests |
| private-cloud-management | [decisions.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/decisions.md) |
| isvara | [PLAN.md](https://github.com/e1-rahabok/isvara/blob/main/PLAN.md) |

One entry each, newest at the bottom. A changed decision is edited in place; git keeps the history.

| ID | Date | Decision | Reason |
|---|---|---|---|
| W-001 | 2026-11-25 | Agent E2 is the source of all domain knowledge: KPI names, parts, limits, thresholds, flows and explanations. PCM-Adapter implements the KPIs. PCM and isvara.io consume. A change to domain knowledge starts in agent-e2. | One master. Every other copy is generated from it or checked against it (CONTRACTS, C1). |
| W-002 | 2026-11-25 | Stage 1 only. PCM is a demo in the lab, and Agent E2 uses a cloud model through Vercel AI Gateway. A customer's on-premises deployment with a local model is stage 2 and out of scope. | Two futures in one plan confuse every session. Stage 2 text stays in the child repositories as the target. |
| W-003 | 2026-11-25 | PCM keeps synthetic ACME data and adds the live lab VCF Operations as a choice, "Live VCF Operations", in the demo control. | The lab has too little activity to show Agent E2. Live mode proves PCM reads real data. |
| W-004 | 2026-11-25 | PCM (private) and isvara.io (public) are two web apps. Both use Agent E2 for knowledge, through the same Vercel AI Gateway. isvara.io connects to no live system. Agent E2 replaces AskIO on isvara.io. | One knowledge service. Agent E2 uses a cheaper model than AskIO. |
| W-005 | 2026-11-25 | isvara.io's content will come from the Agent E2 knowledge base, not from the Word and Excel files. The guide, the tools and the assessment pages are rebuilt. | One master (W-001). |
| W-006 | 2026-11-25 | isvara.io gets an exam for people: 10 short, very hard questions that test depth of understanding, not calculation. It is separate from Agent E2's benchmark, which tests the machine. | A people's exam and a machine benchmark have different purposes. |
| W-007 | 2026-11-25 | VCF-vCommunity-Adapter is renamed PCM-Adapter (the repository). The metric key prefix `vCommunity\|` does not change unless Q-2 decides otherwise. | PCM D-096: the adapter is part of PCM. Keys are kept: changing them breaks history and content in VCF Operations. |
| W-008 | 2026-11-25 | Each repository keeps its own decision log. This file holds only decisions that bind more than one repository, plus the index above. | A cross-repo session needs one place to look; a single-repo session already has its own. |
| W-009 | 2026-11-25 | Git workflow: see [CLAUDE.md](CLAUDE.md), section Git. One branch and pull request per change per repository. While the project is early (defining scope and documentation), Claude merges every pull request itself once the checks pass, and warns the author about a major change in the pull request text and in its report. Revisit when the products have users. | The author, 2026-11-25: early work is mostly scope and documentation, so waiting for review costs more than it saves. The warning keeps the author aware of what spreads to other repositories. |
| W-010 | 2026-11-25 | Contracts between repositories are checked by code in `checks/`. A pull request that breaks a check is not merged. Known gaps are a baseline that only shrinks. | A contract without a check drifts. |
| W-011 | 2026-11-25 | Lab credentials. On the author's laptop: DPAPI files in `$HOME\.secrets\` (`Export-Clixml`), as for vCenter; VCF Operations is `vcf-ops-10.115.1.81.xml`, a read-only account. On the PCM lab VM: `/etc/pcm/pcm.env`, root and group `pcm` only. | Matches what the PCM-Adapter tools and the PCM deployment already use. Windows Credential Manager is no safer for the same user, and the PCM VM runs Linux. |
