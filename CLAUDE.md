# CLAUDE.md

Rules for Claude in work across the repositories. Inside one repository, its own CLAUDE.md also applies. IDs: [spec/glossary.md](spec/glossary.md). All sections but the last hold the method; the last holds this project's rules.

## Order of work

- Work only on the earliest milestone in [ROADMAP.md](ROADMAP.md) that is not done (WD-039). The hook in [.claude/settings.json](.claude/settings.json) prints it at every prompt.
- When a request belongs to a later milestone: list it as parked, in one line, and act on nothing in it.
- When the author makes a suggestion: reply with strengths, weaknesses, gaps and a recommendation. Write to a repository only after the author agrees, or says "do it" or "decide".
- Write `: done` on a milestone's heading only after the author approves it, from its review page [spec/review](spec/review)`/M<n>.md` when it has one.

## Before acting

- Read ROADMAP.md, the files the request touches, and the CLAUDE.md of each repository it touches.
- Before asking the author: search DECISIONS.md, the glossary and the interview records, and quote what they say.
- Decide what the code, the documents or knowledge of the field settle, and state the decision. Ask the author only about judgement, experience, scope and taste.
- Verify a claim from an audit, a review or another session against the files. Report a contradiction with both sources.

## Replies to the author

- Bullet points and short sentences. Each name in full on first use.
- Separate what you know, what you believe and what you have not checked. Disagree when there is a reason.
- Describe how two parts relate by mechanism: code, network, data, dependency or contract.

## Stop and ask

Stop the line of work, add a question with a recommendation and an empty `Answer:` line to [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md), and tell the author, when:

- the specification does not decide something, or two documents disagree;
- a requirement cannot be tested as written;
- a fix would change a contract's shape or reverse a decision;
- a test needs a system that cannot be reached. Report the test as not run.

## Requirements

- Every requirement cites the question or decision it comes from.
- The workspace holds requirements only for contracts, their checks and its own tools (WD-036). Everything else goes in the repository that implements it.
- Before writing a requirement on existing behaviour: read the code that implements it.

## Tests and checks

- Never weaken, skip, delete or loosen a test or a check. A failure is a bug to fix or a question for the author.
- Before and after changing anything in [CONTRACTS.md](CONTRACTS.md): run `uv run checks/run_all.py` with the changed branch checked out.
- Change a contract in three steps: add the new shape, move each consumer, remove the old shape.
- Give every new contract a check, or a ROADMAP line that adds one. Add a gap to a check's baseline only with a question in OPEN-QUESTIONS.md.
- Before each commit: run and pass `python tools/milestone_gate.py --check origin/main`, [`tools/milestone_review.py`](tools/milestone_review.py), [`tools/docs.py`](tools/docs.py), [`tools/style.py`](tools/style.py) and [`tools/spec_check.py`](tools/spec_check.py).

## Writing

- Machine documents: the CLAUDE.md files, [`spec/requirements`](spec/requirements), [`tutorial/templates`](tutorial/templates). One rule or fact per bullet, trigger before action, exact names, no history.
- All other documents, commit messages and pull request text are for people (WD-023). Follow agent-e2's [writing.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/writing.md). Reread each changed line for slogans and "X, not Y": [tools/style.py](tools/style.py) cannot find them.
- Every file reference a link. Every diagram drawn by [tools/diagrams.py](tools/diagrams.py). Every ID with its meaning or a glossary link on first use (WD-020). Each paragraph on one source line.
- A new ID prefix, term or heading must be guessable from itself and overlap no existing one. When a name stops being true: rename it in every file.

## Decisions, questions and Git

- A decision or question that binds several repositories goes in [DECISIONS.md](DECISIONS.md) or OPEN-QUESTIONS.md; one inside a repository goes in that repository (WD-019).
- One branch and one pull request per change per repository; across repositories, the same branch name, each pull request linking the others. Mark finished ROADMAP lines with their pull request.
- Merge your own pull request once its checks pass (WD-009). Never while they are pending or failing. Never push to a default branch. Delete the branch after the merge.
- Put a warning at the top of the pull request and the report when a contract's shape changes, a decision changes, files are deleted, or more than one child repository changes.
- Wait for the author before deleting data. Never print, log or commit a credential.

## Session end

- Add the session's lessons to [tutorial/12-case-study.md](tutorial/12-case-study.md) and the chapter each belongs to.
- When work remains: give the author a prompt for the next session: files to read, settled scope, tasks, how to report.

## This project

- Release 1.0 only (WD-002): a lab demo on a cloud model. Build nothing toward the on-premises deployment with a local model; keep the text that describes it.
- Change domain knowledge (a KPI, threshold, formula, scoring model or explanation) in agent-e2 first (WD-001). Before writing a requirement on existing behaviour, also read the Agent E2 knowledge file that explains it.
- Merge in ownership order: agent-e2, PCM-Adapter, private-cloud-manager, isvara.
- Work on GitHub through clones. Use the author's laptop only for Windows tools and the lab (VPN): PCM-Adapter's build, install and validation tools, and live VCF Operations.
- Wait for the author before changing the lab. Stay read-only against VCF Operations and vCenter unless the milestone says otherwise.
- Credentials: on the laptop, `Import-Clixml` from DPAPI files in `$HOME\.secrets\`; on the PCM lab VM, `/etc/pcm/pcm.env`.
