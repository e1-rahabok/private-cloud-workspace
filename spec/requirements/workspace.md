# Requirements: the workspace

What keeps the repositories one integrated set: the contract checks, the specification's own checks, and the documentation rules. All belong to milestone M2, except R-WS-008 (the gateway check), in M3. Question IDs (Q-) point at the author's answers in the [interview, round 1](../author-input/interview-round-1.md); other IDs are explained in the [glossary](../glossary.md).

### R-WS-001 Every contract has an automated check

Why: a contract no code checks breaks without notice, and the author expects every contract checked.

Source: Q-WS-I1 ("I expect you to check all the contracts"); DESIGN-5.

- Given a contract listed in [contracts](../design/system.md#contracts)
- When the checks run
- Then the contract has a check that fails when its two sides disagree
- And each check has been shown to fail on a planted break

Test scenarios:
- T-WS-001a (anywhere, automated by tools/spec_check.py, to extend): every row of the contracts table names an existing check file, or is marked planned with a milestone.
- T-WS-001b (anywhere, automated once per check): plant a break of each kind the check compares, run the check, and keep the plant as a test in `contract-checks/test_<check>.py`, which CI runs.

### R-WS-002 The checks run where a break would happen

Why: a break costs least when it fails the pull request that causes it, before merge.

Source: DESIGN-5; Q-WS-I1.

- Given a pull request in this repository or in any child repository
- When it is opened or updated
- Then the cross-repo checks run on it with the pull request's branch in place of that repository's main
- And they also run daily on main, and on demand
- And isvara, the one private repository, runs them in its own CI with the four public repositories checked out, because the workspace's CI cannot read isvara without a token

Test scenarios:
- T-WS-002a (anywhere, automated by GitHub Actions): a pull request in each child repository, isvara included, shows the cross-repo checks as a status; each child calls [.github/workflows/cross-repo.yml](../../.github/workflows/cross-repo.yml).
- T-WS-002b (anywhere, manual once per repository): open a pull request in agent-e2 that changes one catalog limit; expect the KPI definitions check to fail on that pull request, before merge; done 2026-11-27 in [agent-e2#489](https://github.com/e1-rahabok/agent-e2/pull/489), closed unmerged.

### R-WS-003 Every requirement is tested, and every test has a requirement

Why: a requirement without a test, or a test without a requirement, hides what the product does.

Source: DESIGN-8; Q-WS-I1.

- Given the requirement files of every repository, in the folders [tools/requirement_files.py](../../tools/requirement_files.py) names (DESIGN-4)
- When the specification check runs
- Then every requirement has a unique ID, a Why line, a Source line that names an existing question, brief item or design choice, and at least one test scenario
- And every test scenario belongs to an existing requirement and says where it runs (anywhere or lab)

Test scenarios:
- T-WS-003a (anywhere, automated by tools/spec_check.py): a requirement without a Why line in this repository, a requirement without a scenario, a scenario without a requirement, a duplicate ID or a Source that names no existing ID fails the check.

### R-WS-004 Documents work for people and for machines

Why: people read these files on GitHub and machines read the same files; an unlinked path or a picture without text serves only one of them.

Source: the author's message of 2026-11-25 on links and diagrams; Q-WS-46.

- Given any Markdown file in this repository
- When the documentation check runs
- Then every file reference is a clickable link
- And every diagram is an SVG drawn by a script, with its text generated underneath
- And every arrow in a diagram starts and ends on a box
- And every relative link resolves

Test scenarios:
- T-WS-004a (anywhere, automated by tools/docs.py --check and tools/diagrams.py in CI): an unlinked path, a stale diagram text or a broken link fails.
- T-WS-004b (anywhere, manual, done 2026-11-26): move one arrow's end off its box; expect tools/docs.py --check to fail and name the diagram.

### R-WS-005 No bare short names

Why: a short name without its meaning makes the reader stop and search.

Source: Q-WS-46.

- Given a document in this repository
- When it uses an ID such as C3, DESIGN-5 or Q-WS-27
- Then on its first use in that document it gives the meaning, or links to the [glossary](../glossary.md)

Test scenarios:
- T-WS-005a (anywhere, manual by a fresh reviewer for each pull request): read the changed files and list every ID used without its meaning. A check is not planned: the rule needs judgement about what a reader already knows.

### R-WS-006 One set of writing rules, checked in every repository

Why: two copies of the rules drift apart, and a rule no code checks is forgotten.

Source: DESIGN-7.

- Given the general writing rules (plain sentences, the flagged phrases, noun-phrase headings, short table cells) and the list of flagged phrases
- When any repository's documents for people are checked
- Then the rules and the list exist once, in this workspace
- And agent-e2's writing rules keep only what is particular to knowledge files, and link to the general ones
- And each repository runs [tools/style.py](../../tools/style.py) on its pull requests
- And each problem the first run finds is fixed in M2, or listed in that repository's baseline, which may only shrink, with one question per repository that names its list, in that repository's question file; a repository without one starts it, with IDs of the form Q-ADP-n, Q-PCM-n or Q-ISVARA-n, as CLAUDE.md requires for a baseline

Test scenarios:
- T-WS-006a (anywhere, automated by tools/style.py in each repository's CI): a pull request that adds a flagged phrase or a sentence heading to a document for people fails; one that fixes a known problem passes and lowers the baseline.
- T-WS-006b (anywhere, automated by a check to write in agent-e2's lint): agent-e2's list of flagged phrases is read from this workspace; a copy of the list in agent-e2 fails.

### R-WS-007 Folder and file names carry no version, milestone or status word

Why: a version or status word in a name stops being true and misleads the next reader.

Source: DESIGN-6; CONSTRAINT-2 (the shipped content keeps its names).

- Given the tracked folders and files of agent-e2, PCM-Adapter, private-cloud-manager, isvara and this workspace, outside archives and dated records
- And outside names that are titles written for readers or for the model, which describe their content and keep it true: agent-e2's [`knowledge/`](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge) and [`benchmark/questions/`](https://github.com/e1-rahabok/agent-e2/tree/main/benchmark/questions), the adapter's shipped `Management Pack/content/` (CONSTRAINT-2), and the review pages `spec/review/M<n>.md`, each named for the milestone it reviews
- When the name check runs
- Then no folder or file name contains, as a whole word between separators, a version (v2, v5), a milestone (m5) or a status word (proto, new, old, final, copy); `thresholds-performance.yaml` does not match "old"
- And each problem the first run finds is renamed in M2, or listed in a baseline that may only shrink, with one question per repository that names its list, in that repository's question file; a repository without one starts it, with IDs of the form Q-ADP-n, Q-PCM-n or Q-ISVARA-n

Test scenarios:
- T-WS-007a (anywhere, automated by [tools/file_names.py](../../tools/file_names.py), run by run_all.py and in each repository's CI; planted breaks in [tools/test_file_names.py](../../tools/test_file_names.py)): a pull request that adds `report_v2.md` or `story_m5.py` fails; one that adds `knowledge/…/why-a-new-framework.md` or `spec/review/M9.md` passes; one that renames a known problem passes and lowers the baseline.
- T-WS-007b (anywhere, manual by a fresh session, once per repository): the session is told it knows the field but not the repository's framework, as the author reads it (DESIGN-6). Given only the repository's folder tree, it writes what it expects in each top-level folder and in each folder one level down, then opens them. Each wrong guess becomes a rename in the same milestone, or a row in the README's folder map where a framework fixes the name.

### R-REPO-006 No repository uses an old repository name

Milestone: M2.

Why: an old name sends a reader or a link to a repository that no longer exists.

Source: Q-WS-3 (round 1: rename references, archives left as they are); CONSTRAINT-2; CONSTRAINT-3.

- Given the repositories agent-e2, PCM-Adapter, private-cloud-manager, isvara and this workspace
- When their files outside archives and dated records are searched, and outside the files that name the old names to forbid them (requirement files and the author's recorded input)
- Then none contains "VCF-vCommunity-Adapter" or "private-cloud-management"

Test scenarios:
- T-REPO-006a (anywhere, automated by [tools/forbidden_names.py](../../tools/forbidden_names.py), run by run_all.py; planted breaks in [tools/test_forbidden_names.py](../../tools/test_forbidden_names.py)): search the clones for the two old names outside archives, dated records and the files that forbid them; expect no match.


### R-WS-010 No repository holds a lab address, host name or credential

Why: four of the five repositories are public, and the lab's addresses and its VM's host name were written in the system design, the glossary, PCM's lab tools and the adapter's tools. A rule in the adapter's CONTRIBUTING.md forbade it for code only, and no check enforced it.

Source: the author, 2026-11-28 ([round 6](../author-input/interview-round-6.md#lab-addresses-in-github)); DESIGN-9.

- Given the tracked text files of the five repositories, outside the author's books as isvara.io serves them
- When they are searched
- Then none holds an IPv4 address in a private range outside the example network 10.20.0.0/16
- And none holds a name listed in `LAB_PRIVATE_NAMES`, when that variable is set from `$HOME\.secrets\lab.json`
- And a lab tool reads every address and host name from `$HOME\.secrets\lab.json` on the laptop, or `/etc/pcm/pcm.env` on the lab VM
- And the check's report names the file and line, never the value

Test scenarios:
- T-WS-010a (anywhere, automated by [tools/lab_addresses.py](../../tools/lab_addresses.py), run by run_all.py on every pull request of every repository; planted breaks in [tools/test_lab_addresses.py](../../tools/test_lab_addresses.py)): an address in each private range, and one inside a file name, fails; an example-network address, a version number, a documentation or public address and the books pass; a listed name fails; the report holds no address.

### R-WS-011 No repository holds a token, key or password

Why: isvara is private on a free plan, where GitHub runs no secret scanning, and a secret pushed to any of the five repositories is copied to every clone at once.

Source: DESIGN-26.

- Given the tracked text files of the five repositories
- When they are searched
- Then none holds a GitHub, OpenAI, Anthropic, AWS, Slack or Vercel token, a private key, or a password, token or key written as a quoted value
- And a value that is clearly an example (a placeholder, `...`, or the documented sample password of a vendor's example file) passes
- And the check's report names the file and line, never the value

Test scenarios:
- T-WS-011a (anywhere, automated by [tools/secret_values.py](../../tools/secret_values.py), run by run_all.py on every pull request of every repository; planted breaks in [tools/test_secret_values.py](../../tools/test_secret_values.py)): a planted token of each kind, a private key and a quoted password fail; a placeholder and an environment-variable reference pass; the report holds no value.

### R-WS-012 Every repository keeps its dependencies and workflows safe

Why: on 2026-11-28 isvara.io ran a Next.js release with a critical advisory and no alert reported it, and one workflow ran with the default token rights.

Source: DESIGN-25, DESIGN-26.

- Given the five repositories
- When their workflows and dependency files are read
- Then every workflow declares `permissions` at its top level
- And every action outside `actions/` and the workspace's own workflows is pinned to a full commit hash
- And every repository has a [`.github/dependabot.yml`](../../.github/dependabot.yml) that covers GitHub Actions and each package system it holds (npm with a [`package-lock.json`](https://github.com/e1-rahabok/isvara/blob/main/package-lock.json), pip with a `requirements.txt`)
- And isvara.io's CI fails when `npm audit --omit=dev --audit-level=high` finds an advisory

Test scenarios:
- T-WS-012a (anywhere, automated by [tools/workflows.py](../../tools/workflows.py), run by run_all.py; planted breaks in [tools/test_workflows.py](../../tools/test_workflows.py)): a workflow with no permissions, a third-party action on a tag, and a repository with a lockfile but no npm entry in `dependabot.yml` each fail; GitHub's own actions on a major tag pass.
- T-WS-012b (anywhere, automated by the npm audit step of [cross-repo.yml](../../.github/workflows/cross-repo.yml)): on a repository with a [`package-lock.json`](https://github.com/e1-rahabok/isvara/blob/main/package-lock.json), a high advisory in a production dependency fails the run.

### R-WS-013 Each milestone review rereads the security baseline

Why: a check finds only what it was written for; the baseline names the threats no check covers yet (DESIGN-24).

Source: DESIGN-24.

- Given a milestone's review
- When Claude prepares the review page
- Then each row of the system design's section Security baseline is read against the repositories, and every gap is either fixed or written into the specification with its reason

Test scenarios:
- T-WS-013a (anywhere, manual, at each milestone review): the review page lists the baseline rows read and the gaps found; expect each gap to name the requirement or design choice that now covers it. A check is not planned: it needs judgement about what a row asks.

### R-WS-014 No branch that main holds stays on GitHub

Why: a cloud session cannot delete a branch (CONSTRAINT-9), and the author reads only `main` and has no time to review a list of leftover branches (CONSTRAINT-8).

Source: DESIGN-28; the author's corrections of 2026-11-28 ([round 6](../author-input/interview-round-6.md), section Branches).

- Given a branch other than `main` in any of the five repositories
- When the branch cleanup runs, every day, on every push to `main` and on demand
- Then the branch is deleted when it is not ahead of `main`
- And it is kept, with its reason, when it is protected, on the repository's keep list, the head of an open pull request, ahead of `main`, or without history in common with `main`
- And the run lists each deleted branch with its last commit, and each kept branch ahead of `main` with its number of commits ahead
- And on a pull request the run deletes nothing and lists what it would delete
- And a deletion GitHub refuses fails the run
- And every repository has a workflow that calls the branch cleanup, and only the job that deletes has write rights

Test scenarios:
- T-WS-014a (anywhere, automated by [tools/test_branch_cleanup.py](../../tools/test_branch_cleanup.py), against a fake GitHub): a branch of each kind to keep is kept with its reason; a branch not ahead of `main` is deleted and listed with its commit; a dry run deletes nothing; a refused deletion fails the run.
- T-WS-014b (anywhere, automated by [tools/workflows.py](../../tools/workflows.py), run by run_all.py; planted break in [tools/test_workflows.py](../../tools/test_workflows.py)): a repository with no workflow that calls the branch cleanup fails.
- T-WS-014c (anywhere, manual, once after the first run in each repository): list its branches; expect none that is not ahead of `main` apart from the kinds kept, and the run's list to name each deleted branch with its last commit.

### R-WS-009 Project documents agree with the specification

Why: the READMEs and CLAUDE-PROJECT.md files were written before the specification and were never read against it, so a fact in them can contradict it, or state what the specification never decided, and a reader or a session acts on it. isvara's README said the books come from Box; the books come from the author's laptop (DEPENDENCY-10).

Source: the author, 2026-11-28 ([round 6](../author-input/interview-round-6.md), "Corrections"); DESIGN-8.

- Given the README.md and CLAUDE-PROJECT.md of each of the five repositories
- When a reviewer reads each statement of fact about the product: where data comes from, who provides it, what runs where, and what a part does
- Then each one agrees with the brief, the system design, a requirement or the code
- And a fact the specification does not hold is added to it first, then the document is changed to match

Test scenarios:
- T-WS-009a (anywhere, manual by a fresh reviewer, once in M2 and for each pull request that changes one of these files): read the files against the specification and list every statement that disagrees with it or that it does not hold; expect an empty list after the fixes. A check is not planned: it needs judgement about what is a fact.

### R-WS-008 The model gateway answers the model Agent E2 is set to

Why: Agent E2 fails in the demo when the model it is set to no longer answers at the gateway.

Source: DESIGN-5 (every contract has a check); GOAL-4 (every contract is checked automatically); C5, the model gateway, in [contracts](../design/system.md#contracts).

Milestone: M3.

- Given the Vercel AI Gateway key in the environment
- When `contract-checks/model_gateway.py` runs
- Then it sends one short question to the model named in agent-e2's `service_config.yaml` and expects an answer with text
- And without the key it reports "not run", never "passed"

Test scenarios:
- T-WS-008a (anywhere with the gateway key, automated by `contract-checks/model_gateway.py`, to write, run by [`contract-checks/run_all.py`](../../contract-checks/run_all.py)): the configured model answers; a model ID that does not exist fails and names the ID.
## Questions for round two

- None.
