# Private Cloud Workspace

The parent repository of four repositories that are built and tested as one integrated set. It holds what no single repository can: how the parts fit, the contracts between them, the decisions that bind more than one of them, the roadmap, and the code that checks the contracts.

## The repositories

| Repository | What it is | Owns |
|---|---|---|
| [agent-e2](https://github.com/e1-rahabok/agent-e2) | The knowledge service. No UI. Answers like a VMware expert, over HTTP. | All domain knowledge: KPI definitions, thresholds, flows, explanations |
| [PCM-Adapter](https://github.com/e1-rahabok/PCM-Adapter) | The VCF Operations management pack (formerly VCF-vCommunity-Adapter). Computes the KPIs inside VCF Operations. | The KPIs Agent E2 defines; the objects and metrics it needs |
| [private-cloud-manager](https://github.com/e1-rahabok/private-cloud-manager) | PCM, a private web app for operations roles. Runs in the lab.    | Screens, roles, data connections, actions |
| [isvara](https://github.com/e1-rahabok/isvara) | isvara.io, a public web app for learning the domain. Private repository. | Public reading and vCommunity feedback, books dowload, tools and exam pages |

PCM and isvara.io are two web apps. Both get their knowledge from Agent E2. [SYSTEM.md](SYSTEM.md) has the whole picture.

## The files here

| File | Holds |
|---|---|
| [SYSTEM.md](SYSTEM.md) | The parts, how data and questions flow, the lab, what is in scope (release 1.0) |
| [CONTRACTS.md](CONTRACTS.md) | Every interface between two repositories: owner, consumer, shape, the check that proves it |
| [DECISIONS.md](DECISIONS.md) | Decisions that bind more than one repository |
| [ROADMAP.md](ROADMAP.md) | The whole plan on one page: goal, release 1.0, milestones, what waits for the author |
| [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) | The questions only the author can answer |
| [`spec/`](spec) | The specification: intent, then requirements with test scenarios |
| [`tools/`](tools) | Keep the documents readable by people and machines: clickable links, SVG diagrams with generated text |
| [CLAUDE.md](CLAUDE.md) | How Claude works across the repositories |
| [`checks/`](checks) | The cross-repo checks |
| [`tutorial/`](tutorial) | How this workspace is built with AI, written to teach the method to others |

## Run the checks

Clone the repositories next to this one, or let the script clone what is missing:

```powershell
uv run checks/run_all.py
```

Without uv: `pip install pyyaml requests`, then `python checks/run_all.py`. Add `--pull` to update the clones first. To test a branch of a child repository before merging it, check that branch out in its clone and run without `--pull`.

GitHub Actions runs the same checks on every push and pull request here, every day, and on demand ([checks workflow](.github/workflows/checks.yml)).
