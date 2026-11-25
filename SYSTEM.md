# System

How the four repositories work as one system. Current state, stage 1. For people and for Claude.

## Two web apps, one knowledge service

```
                       Vercel AI Gateway (model)
                          ^                ^
                          |                |
   PCM (private, lab) --> Agent E2         Agent E2 <-- isvara.io (public)
          |                                             no live system
          v
   VCF Operations  <-- PCM-Adapter computes the KPIs inside it
   (synthetic ACME data, or the live lab instance)
```

| Part | Repository | Runs where | Talks to |
|---|---|---|---|
| PCM | private-cloud-management | Lab Linux VM moltbot29, https://10.114.1.29 (VPN) | Agent E2 over HTTP; VCF Operations Suite API (live mode) |
| Agent E2 for PCM | agent-e2 | Same lab VM, port 8090, as a systemd service | Vercel AI Gateway |
| PCM-Adapter | PCM-Adapter | Inside the lab VCF Operations, https://10.115.1.81 (VPN) | vCenter, VCF Operations |
| isvara.io | isvara | Vercel, public | Agent E2 (planned, ROADMAP M5); today its own AskIO agent |
| Agent E2 for isvara.io | agent-e2 | Not decided (OPEN-QUESTIONS, Q-4) | Vercel AI Gateway |

## Where each kind of thing comes from

| Thing | Source | Used by |
|---|---|---|
| KPI definitions: names, parts, limits, bands | Agent E2 catalog, `knowledge/catalog/thresholds-*.yaml` | PCM-Adapter implements them; PCM shows them; Agent E2 explains them |
| KPI values | PCM-Adapter, published in VCF Operations under `vCommunity\|` | PCM, through the Suite API (live mode) |
| Synthetic values | PCM's generator, `build/pcm_proto/` | PCM demo mode |
| Explanations and answers | Agent E2 | PCM's Agent E2 panel; isvara.io (planned) |
| Reading content | Today: the Word books. Planned: the Agent E2 knowledge base | isvara.io |

## PCM data modes

PCM keeps both, chosen from the demo control at the top of every page:

- **Synthetic ACME** (default): a global bank with stories written relative to now. It shows Agent E2 at its best.
- **Live VCF Operations** (ROADMAP M2): the lab instance. It proves PCM reads real data; the lab is too quiet to show Agent E2 well.

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
| private-cloud-management | The unit tests in `build/tests/test_*.py`, for example `python3 -m unittest build.tests.test_executive -v`; page tests need Playwright ([build/README.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/build/README.md)) | Install on the lab VM: [deploy/README.md](https://github.com/e1-rahabok/private-cloud-management/blob/main/deploy/README.md) |
| isvara | `npm run lint`, `npm run typecheck`, `npm run build`, `npm run test:rvtools` | `npm run eval` and `eval:injection` need a running server and the gateway key |
| All four together | `uv run checks/run_all.py` (this repository) | |
