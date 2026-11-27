# CLAUDE.md

Rules for Claude in work that crosses the repositories. Inside one repository, that repository's CLAUDE.md also applies. IDs: [spec/glossary.md](spec/glossary.md).

## Session start

- Read [SYSTEM.md](SYSTEM.md), [CONTRACTS.md](CONTRACTS.md), [ROADMAP.md](ROADMAP.md) and the requirement files the request touches.
- Name the milestone and the requirement IDs. If the request belongs to none, say so before starting.
- Read the CLAUDE.md of each repository the change touches.
- Work on GitHub through clones. Use the author's laptop only for Windows tools and the lab (VPN): PCM-Adapter's build, install and validation tools, and live VCF Operations.

## Thinking

- Treat the author's suggestion as input. Unless the author says "decide" or "do it": reply with strengths, weaknesses, gaps and a recommendation; write to a repository only after agreement.
- Disagree when there is a reason. Separate what you know, what you believe and what you have not checked.
- Decide anything that the code, the documents or general knowledge of the field settles, and state the decision. Ask the author only about judgement, field experience, scope and taste.

## Specification first

- Start no build milestone before its requirements and test scenarios exist in [spec/requirements](spec/requirements) and the author has approved them.
- Every requirement cites the question or decision it comes from. Never write a requirement from a guess.

## Stop conditions

Stop the line of work, add a question with a recommendation and an empty `Answer:` line to [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md), and tell the author, when:

- the specification does not decide something, or two documents disagree;
- a requirement cannot be tested as written;
- a fix would change a contract's shape or reverse a decision;
- a test needs the lab and the lab cannot be reached. Report the test as not run.

## Scope

- Release 1.0 only (WD-002): a lab demo on a cloud model. Build nothing toward the on-premises deployment with a local model; keep the text that describes it.
- Change domain knowledge (a KPI, threshold or explanation) in agent-e2 first (WD-001).

## Tests and checks

- Never weaken, skip, delete or loosen a test or a check to make it pass. A failure is a bug to fix or a question for the author.
- Before and after changing anything in CONTRACTS.md: run `uv run checks/run_all.py` with the changed branch checked out in its clone.
- Change a contract in three steps: add the new shape, move each consumer, remove the old shape.
- Add a known gap to a check's baseline only together with a question in OPEN-QUESTIONS.md.
- Give every new contract a check, or a ROADMAP line that adds one.

## Writing

Two kinds of document (WD-023):

- For people: README.md, SYSTEM.md, CONTRACTS.md, DECISIONS.md, ROADMAP.md, OPEN-QUESTIONS.md, spec/intent.md, spec/glossary.md, spec/design, tutorial, commit messages, pull request text.
  - Follow agent-e2's [writing.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/writing.md) and its `avoid_ai_speak` list: plain sentences; no flagged phrase, slogan or "X, not Y"; headings as noun phrases of at most 9 words; table cells of about 12 words, else bullets.
  - Reread each changed line with the lines around it for slogans and "X, not Y"; no script finds them.
- For machines: the CLAUDE.md files, spec/requirements, tutorial/templates.
  - One rule or fact per bullet. Trigger before action. Exact paths, names and IDs. No history or attribution.
- Before adding an ID prefix, term, heading or numbering: make it guessable from itself, with one word per concept and no overlap with an existing one.
- When a name or number stops being true: rename it in every file. Never add text that explains the exception.
- In both: every file reference a link; every diagram an SVG drawn by [tools/diagrams.py](tools/diagrams.py) with its text generated underneath; every ID with its meaning or a glossary link on first use (WD-020).
- Before each commit, run and pass: `python tools/docs.py`, `python tools/style.py`, `python tools/spec_check.py`.

## Session end

- Before reporting a session as finished: add its lessons to [tutorial/12-case-study.md](tutorial/12-case-study.md) and to the tutorial chapter each lesson belongs to.
- When work remains: give the author a prompt for the next session, with the files to read, the settled scope, the tasks and how to report.

## Decisions and questions

- Record a decision that binds several repositories in [DECISIONS.md](DECISIONS.md), one block per decision. Record a decision inside one repository in that repository's log.
- Write a question about one repository in that repository; a question that binds several in OPEN-QUESTIONS.md (WD-019).
- Mark finished ROADMAP lines with their pull request.

## Git

- One branch and one pull request per change per repository. Across repositories: the same branch name in each, and each pull request links the others.
- Merge in ownership order: agent-e2, PCM-Adapter, private-cloud-manager, isvara.
- Merge your own pull request once its checks have reported and passed (WD-009). Never merge while checks are pending or failing.
- Put a warning at the top of the pull request and in the report when the change is major: a contract's shape changes; a decision is added, changed or reversed; files are deleted or archived; or more than one child repository changes.
- Wait for the author before anything that deletes data or changes the lab.
- Never push to a default branch. Delete the branch after the merge.

## Secrets and the lab

- Load laptop credentials with `Import-Clixml` from DPAPI files in `$HOME\.secrets\`. On the PCM lab VM they are in `/etc/pcm/pcm.env`.
- Never print, log or commit a credential, or copy one into a repository.
- Stay read-only against VCF Operations and vCenter unless the milestone says otherwise.
