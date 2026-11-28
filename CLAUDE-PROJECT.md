# CLAUDE-PROJECT.md

Rules, tools and paths of this project: Private Cloud Manager and its repositories, coordinated from private-cloud-workspace. Loaded with [CLAUDE.md](CLAUDE.md), which holds the method. IDs: [spec/glossary.md](spec/glossary.md).

## Files of the method

- Roadmap: [ROADMAP.md](ROADMAP.md). The milestone gate is [tools/milestone_gate.py](tools/milestone_gate.py), run at every prompt by the hook in [.claude/settings.json](.claude/settings.json).
- Specification map: [spec/README.md](spec/README.md). The author's input, word for word: [spec/author-input/](spec/author-input). Input still needed: [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).
- Goals, users, scope, principles, constraints, assumptions, risks, dependencies: [spec/brief.md](spec/brief.md).
- Requirements: [spec/requirements](spec/requirements). Review pages: [spec/review](spec/review)`/M<n>.md`.
- System design, contracts C1 to C5 and design choices: [spec/design/system.md](spec/design/system.md). Test plan: [spec/test-plan.md](spec/test-plan.md).
- Before acting, also read [spec/brief.md](spec/brief.md) and [spec/design/system.md](spec/design/system.md).

## Checks before each commit

- `python tools/milestone_gate.py --check origin/main`
- `python tools/claude_md_copies.py`: every child repository has this CLAUDE.md and its own CLAUDE-PROJECT.md. CI checks all but isvara, which it cannot read.
- `python tools/milestone_review.py`, `python tools/docs.py`, `python tools/style.py`, `python tools/spec_check.py`
- Before and after changing a contract in [spec/design/system.md](spec/design/system.md), section Contracts: `uv run contract-checks/run_all.py`, with the changed branch checked out in its clone.

## Writing

- Writing rules: [writing/README.md](writing/README.md) and its list [writing/flagged-phrases.yaml](writing/flagged-phrases.yaml), checked by [tools/style.py](tools/style.py) (DESIGN-7, R-WS-006). Agent E2's knowledge files also follow agent-e2's [writing.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/writing.md).
- Machine documents also include the child repositories' CLAUDE.md files and [`tutorial/templates`](tutorial/templates).
- Every diagram is an SVG drawn by [tools/diagrams.py](tools/diagrams.py), with its text generated underneath (R-WS-004).

## Several repositories

- This workspace holds requirements only for contracts between repositories, their checks and its own tools (DESIGN-4). Everything else goes in the repository that implements it.
- A question or outcome that binds several repositories goes in this workspace; one inside a repository goes in that repository.
- Across repositories: the same branch name in each, and each pull request links the others.
- Merge in ownership order: agent-e2, PCM-Adapter, private-cloud-manager, isvara.
- Merge your own pull request once its checks have reported and passed. The author approved this while the project is early, 2026-11-25.
- Put a major-change warning also when more than one child repository changes.
- When a Dependabot pull request's checks have passed: merge it as your own (DESIGN-25).
- Before reporting a session as finished: delete every branch that is not ahead of `main`, except branches a workflow writes, such as PCM-Adapter's `badges`. The author reads only `main`.
- Never delete a branch that is ahead of `main`: its commits are on no other branch (the author).
- When a pull request left open by an earlier session is overtaken by `main`: close it with a comment that links where its content is now, and keep its branch. When it holds content the specification lacks: list it for the author.
- When a branch cannot be deleted from the session (a cloud session gets HTTP 403): give the author a link to each one, and say how many commits each is ahead of `main`.

## Domain

- Release 1.0 only (SCOPE-1): a lab demo on a cloud model. Build nothing toward the on-premises deployment with a local model; keep the text that describes it.
- Change domain knowledge (a KPI, threshold, formula, scoring model or explanation) in agent-e2 first (DESIGN-2). Before writing a requirement on existing behaviour, also read the Agent E2 knowledge file that explains it.

## The lab

- Work on GitHub through clones. Use the author's laptop only for Windows tools and the lab (VPN): PCM-Adapter's build, install and validation tools, and live VCF Operations.
- Wait for the author before changing the lab. Stay read-only against VCF Operations and vCenter unless the milestone says otherwise.
- Credentials: on the laptop, `Import-Clixml` from DPAPI files in `$HOME\.secrets\`; on the PCM lab VM, `/etc/pcm/pcm.env`.

## Session end

- Before reporting a session as finished: add its lessons to [tutorial/16-case-study.md](tutorial/16-case-study.md) and the chapter each belongs to.
