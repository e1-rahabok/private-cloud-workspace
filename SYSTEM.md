# System

How the four repositories work as one system. Current state, stage 1. For people and for Claude.

## Two web apps, one knowledge service

![The system in stage 1: PCM, Agent E2, VCF Operations with PCM-Adapter in the lab; isvara.io, its planned Agent E2 and the model gateway on the Internet; the contracts C1 to C5 between them](images/system.svg)

<details>
<summary>Text of the diagram, for readers that cannot see it</summary>

Colour key: grey = PCM; blue = Agent E2; green = PCM-Adapter; purple = isvara.io; orange = Model.

Boxes, nested as drawn:
- n1 **PCM** (PCM): Web app for operations roles; synthetic ACME or live data; lab VM, https://10.114.1.29
- n2 **Agent E2 for PCM** (Agent E2): Knowledge service over HTTP; owns all domain knowledge; same lab VM, port 8090
- n3 **isvara.io** (isvara.io): Public learning site; on Vercel; no live system
- n4 **Agent E2 for isvara.io** (Agent E2): Where it runs: OPEN-QUESTIONS Q-4
- n5 **VCF Operations**: Lab, https://10.115.1.81
  - n6 **PCM-Adapter** (PCM-Adapter): Computes the KPIs inside VCF Operations, under vCommunity|
- n7 **Vercel AI Gateway** (Model): Cloud model for stage 1

Arrows (from, to, label):
- n1 PCM --> n2 Agent E2 for PCM: C3
- n1 PCM --> n5 VCF Operations: C2 Suite API, live mode
- n2 Agent E2 for PCM ..> n6 PCM-Adapter: C1 KPI definitions
- n2 Agent E2 for PCM --> n7 Vercel AI Gateway: C5
- n2 Agent E2 for PCM ..> n3 isvara.io: C4
- n3 isvara.io ..> n4 Agent E2 for isvara.io: C3
- n4 Agent E2 for isvara.io ..> n7 Vercel AI Gateway: C5

Notes on the diagram:
- Dashed: planned

Arrows: `-->` solid, `..>` dashed.

</details>

| Part | Repository | Runs where | Talks to |
|---|---|---|---|
| PCM | private-cloud-management | Lab Linux VM moltbot29, https://10.114.1.29 (VPN) | Agent E2 over HTTP; VCF Operations Suite API (live mode) |
| Agent E2 for PCM | agent-e2 | Same lab VM, port 8090, as a systemd service | Vercel AI Gateway |
| PCM-Adapter | PCM-Adapter | Inside the lab VCF Operations, https://10.115.1.81 (VPN) | vCenter, VCF Operations |
| isvara.io | isvara | Vercel, public | Agent E2 (planned, ROADMAP M6); today its own AskIO agent |
| Agent E2 for isvara.io | agent-e2 | Not decided (OPEN-QUESTIONS, Q-4) | Vercel AI Gateway |

## Sources of each kind of data

| Thing | Source | Used by |
|---|---|---|
| KPI definitions: names, parts, limits, bands | Agent E2's [catalog](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge/catalog) | PCM-Adapter, PCM, Agent E2 |
| KPI values | PCM-Adapter, published in VCF Operations under `vCommunity\|` | PCM, through the Suite API (live mode) |
| Synthetic values | PCM's generator, [`build/pcm_proto/`](https://github.com/e1-rahabok/private-cloud-management/tree/main/build/pcm_proto) | PCM demo mode |
| Explanations and answers | Agent E2 | PCM's Agent E2 panel; isvara.io (planned) |
| Reading content | Today: the Word books. Planned: the Agent E2 knowledge base | isvara.io |

## PCM data modes

PCM keeps both, chosen from the demo control at the top of every page:

- **Synthetic ACME** (default): a global bank with stories written relative to now. It shows Agent E2 at its best.
- **Live VCF Operations** (ROADMAP M3): the lab instance. It proves PCM reads real data; the lab is too quiet to show Agent E2 well.

## Stage 1 and stage 2

- **Stage 1 (now, in scope):** PCM is a demo in the lab. Agent E2 uses a cloud model through Vercel AI Gateway. isvara.io is public on Vercel.
- **Stage 2 (out of scope):** a customer deploys PCM and Agent E2 on premises with a local model server. Text in the child repositories about on-premises models describes stage 2. Do not build toward it now; do not remove it either.

## Lab

| Host | What | Access |
|---|---|---|
| 10.114.1.29 (moltbot29) | PCM and Agent E2 | VPN from the author's laptop. Secrets in `/etc/pcm/pcm.env` on the VM |
| 10.115.1.81 | VCF Operations 9 with PCM-Adapter installed | VPN. Laptop credential: `$HOME\.secrets\vcf-ops-10.115.1.81.xml` (DECISIONS, W-011) |
| 10.115.1.87 | vCenter | VPN. Laptop credential: `$HOME\.secrets\vcenter-10.115.1.87.xml` |

## Build and test per repository

| Repository | Runs anywhere | Needs the lab |
|---|---|---|
| agent-e2 | `python3 project/tools/rules_check.py` (0 problems), `python3 -m unittest harness/test_harness.py`, `python3 -m unittest benchmark/runner/test_runner.py` | The benchmark needs the gateway key |
| PCM-Adapter | `python -m pytest tests`, from `Management Pack` | `pwsh tools/build/build.ps1`, `install.ps1`, `restart.ps1`, `validate.ps1` (Windows, PowerShell 7, the lab) |
| private-cloud-management | Unit tests in [`build/tests`](https://github.com/e1-rahabok/private-cloud-management/tree/main/build/tests); page tests need Playwright ([build/README.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/build/README.md)) | Install on the lab VM: [deploy/README.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/deploy/README.md) |
| isvara | `npm run lint`, `npm run typecheck`, `npm run build`, `npm run test:rvtools` | `npm run eval` and `eval:injection` need a running server and the gateway key |
| All four together | `uv run checks/run_all.py` (this repository) | |
