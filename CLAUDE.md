# CLAUDE.md

How Claude works across the four repositories. Each child repository has its own CLAUDE.md for work inside it; this file is for work that crosses them.

## Start of every session

- Read [SYSTEM.md](SYSTEM.md), [CONTRACTS.md](CONTRACTS.md) and [ROADMAP.md](ROADMAP.md). Find the milestone the request belongs to. If it belongs to none, say so before starting.
- Then read the CLAUDE.md of each repository the change touches, and follow it inside that repository.
- Work on GitHub through clones; the author's laptop is for what needs Windows or the lab (VPN): PCM-Adapter's build, install and validation tools, and live VCF Operations.

## Specification first

- No build milestone starts until its requirements are written in [`spec/requirements/`](spec/requirements), each with its test scenarios, and the author has approved them (ROADMAP, M1).
- Requirements come from the author's answers in [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md), never from a guess. A requirement cites the answer or decision it comes from.

## Stop conditions

Stop that line of work, write the question to [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) with a recommendation and an empty `Answer:` line, and tell the author, when:

- the specification does not decide something, or two documents disagree;
- a requirement cannot be tested as written;
- a fix would change a contract's shape or reverse a decision;
- a test needs the lab and the lab cannot be reached: say so, and never report it as passed.

Never weaken, skip, delete or loosen a test or a check to make it pass. A failing test is either a bug to fix or a question for the author.

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
- No bare short names (W-020). On first use in a document, write an ID such as C3, W-012 or Q-27 with its meaning, or as a link to [spec/glossary.md](spec/glossary.md). A new kind of ID goes into the glossary first.
- Write for a reader on GitHub: plain words, short sentences, every file reference a link, every diagram an SVG with its text underneath ([tools/docs.py](tools/docs.py)).

## Git

- One branch and one pull request per change per repository. A change across repositories uses the same branch name in each, and each pull request links the others.
- Merge order follows ownership: agent-e2, then PCM-Adapter, then private-cloud-management, then isvara.
- Claude merges its own pull request once the checks pass (DECISIONS, W-009: the early phase).
- A major change is still merged, with a warning at the top of the pull request text and in the report to the author. Major means: a contract's shape changes, a decision is added, changed or reversed, files are deleted or archived, or the change spans more than one child repository.
- Never merge a pull request whose checks fail. Anything that deletes data or changes the lab waits for the author.
- Never push to a default branch directly. Delete the branch after the merge.
- Commit messages and pull request text describe the change in plain words.

## Secrets and the lab

- Credentials on the laptop are DPAPI files in `$HOME\.secrets\`, loaded with `Import-Clixml`. On the PCM lab VM they are in `/etc/pcm/pcm.env`. Never print, log or commit one, and never copy one into a repository.
- Read-only against VCF Operations and vCenter unless the milestone says otherwise.
