# CLAUDE.md

How Claude works across the four repositories. Each child repository has its own CLAUDE.md for work inside it; this file is for work that crosses them.

## Start of every session

- Read [SYSTEM.md](SYSTEM.md), [CONTRACTS.md](CONTRACTS.md) and [ROADMAP.md](ROADMAP.md). Find the milestone the request belongs to. If it belongs to none, say so before starting.
- Then read the CLAUDE.md of each repository the change touches, and follow it inside that repository.
- Work on GitHub through clones; the author's laptop is for what needs Windows or the lab (VPN): PCM-Adapter's build, install and validation tools, and live VCF Operations.

## Scope

- Stage 1 only (DECISIONS, W-002). Do not build toward the on-premises local model, and do not remove the text that describes it.
- Agent E2 is the source of domain knowledge (W-001). A KPI, threshold or explanation changes in agent-e2 first.

## Contracts and checks

- Before changing anything listed in CONTRACTS.md, run `uv run checks/run_all.py` with the changed branch checked out in its clone, and again after.
- A contract changes by expand, migrate, contract (CONTRACTS.md). Never break a consumer in one step.
- Never weaken a check to make it pass. A new known gap goes in the check's baseline only with an entry in OPEN-QUESTIONS.md.
- A new contract gets a check, or a ROADMAP line that adds one.

## Decisions and questions

- A decision that binds more than one repository goes in [DECISIONS.md](DECISIONS.md). A decision inside one repository goes in that repository's log (index in DECISIONS.md).
- When the specification does not decide something, stop and write the question to [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) with a recommendation. Do not guess.
- Mark finished lines in ROADMAP.md with the pull request.

## Git

- One branch and one pull request per change per repository. A change across repositories uses the same branch name in each, and each pull request links the others.
- Merge order follows ownership: agent-e2, then PCM-Adapter, then private-cloud-management, then isvara.
- Claude merges its own pull request when the checks pass and the change is inside an approved milestone.
- These wait for the author: a change to a contract's shape, a new or changed entry in DECISIONS.md, and anything that deletes data or changes the lab.
- Never push to a default branch directly. Delete the branch after the merge.
- Commit messages and pull request text describe the change in plain words.

## Secrets and the lab

- Credentials on the laptop are DPAPI files in `$HOME\.secrets\`, loaded with `Import-Clixml`. On the PCM lab VM they are in `/etc/pcm/pcm.env`. Never print, log or commit one, and never copy one into a repository.
- Read-only against VCF Operations and vCenter unless the milestone says otherwise.
