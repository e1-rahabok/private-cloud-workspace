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
- T-WS-001b (anywhere, automated once per check): plant a break of each kind the check compares, run the check, and keep the plant as a test in `checks/test_<check>.py`, which CI runs.

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

Source: DESIGN-6, with isvara's renames in M4; CONSTRAINT-2 (the shipped content keeps its names).

- Given the tracked folders and files of agent-e2, PCM-Adapter, private-cloud-manager, isvara and this workspace, outside archives and dated records
- And outside names that are titles written for readers or for the model, which describe their content and keep it true: agent-e2's [`knowledge/`](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge) and [`benchmark/questions/`](https://github.com/e1-rahabok/agent-e2/tree/main/benchmark/questions), the adapter's shipped `Management Pack/content/` (CONSTRAINT-2), and the review pages `spec/review/M<n>.md`, each named for the milestone it reviews
- When the name check runs
- Then no folder or file name contains, as a whole word between separators, a version (v2, v5), a milestone (m5) or a status word (proto, new, old, final, copy); `thresholds-performance.yaml` does not match "old"
- And each problem the first run finds is renamed in M2, or listed in a baseline that may only shrink, with one question per repository that names its list, in that repository's question file; a repository without one starts it, with IDs of the form Q-ADP-n, Q-PCM-n or Q-ISVARA-n

Test scenarios:
- T-WS-007a (anywhere, automated by [checks/file_names.py](../../checks/file_names.py), run by run_all.py and in each repository's CI; planted breaks in [checks/test_file_names.py](../../checks/test_file_names.py)): a pull request that adds `report_v2.md` or `story_m5.py` fails; one that adds `knowledge/…/why-a-new-framework.md` or `spec/review/M9.md` passes; one that renames a known problem passes and lowers the baseline.
- T-WS-007b (anywhere, manual by a fresh session, once per repository): given only the repository's folder tree, the session writes what it expects in each top-level folder and in each folder one level down, then opens them. Each wrong guess becomes a rename in the same milestone; isvara's five are renamed in M4 (DESIGN-6).

### R-REPO-006 No repository uses an old repository name

Milestone: M2.

Why: an old name sends a reader or a link to a repository that no longer exists.

Source: Q-WS-3 (round 1: rename references, archives left as they are); CONSTRAINT-2; CONSTRAINT-3.

- Given the repositories agent-e2, PCM-Adapter, private-cloud-manager, isvara and this workspace
- When their files outside archives and dated records are searched, and outside the files that name the old names to forbid them (requirement files, DECISIONS.md and the interview records)
- Then none contains "VCF-vCommunity-Adapter" or "private-cloud-management"

Test scenarios:
- T-REPO-006a (anywhere, automated by [checks/forbidden_names.py](../../checks/forbidden_names.py), run by run_all.py; planted breaks in [checks/test_forbidden_names.py](../../checks/test_forbidden_names.py)): search the clones for the two old names outside archives, dated records and the files that forbid them; expect no match.


### R-WS-008 The model gateway answers the model Agent E2 is set to

Why: Agent E2 fails in the demo when the model it is set to no longer answers at the gateway.

Source: DESIGN-5 (every contract has a check); GOAL-4 (every contract is checked automatically); C5, the model gateway, in [contracts](../design/system.md#contracts).

Milestone: M3.

- Given the Vercel AI Gateway key in the environment
- When `checks/model_gateway.py` runs
- Then it sends one short question to the model named in agent-e2's `service_config.yaml` and expects an answer with text
- And without the key it reports "not run", never "passed"

Test scenarios:
- T-WS-008a (anywhere with the gateway key, automated by `checks/model_gateway.py`, to write, run by [`checks/run_all.py`](../../checks/run_all.py)): the configured model answers; a model ID that does not exist fails and names the ID.
## Questions for round two

- None.
