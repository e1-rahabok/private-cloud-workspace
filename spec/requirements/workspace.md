# Requirements: the workspace

What keeps the repositories one integrated set: the contract checks, the specification's own checks, and the documentation rules. All belong to milestone M2. Question IDs (Q-) point at the author's answers in the [interview, round 1](../interview-round-1.md); other IDs are explained in the [glossary](../glossary.md).

### R-WS-001 Every contract has an automated check

Source: answer to Q-I1 ("I expect you to check all the contracts"); WD-010.

- Given a contract listed in [CONTRACTS.md](../../CONTRACTS.md)
- When the checks run
- Then the contract has a check that fails when its two sides disagree
- And each check has been shown to fail on a planted break

Test scenarios:
- T-WS-001a (anywhere, automated by tools/spec_check.py, to extend): every row of CONTRACTS.md names an existing check file, or is marked planned with a milestone.
- T-WS-001b (anywhere, manual once per check): plant a break, run the check, record the failure in the check's docstring.

### R-WS-002 The checks run where a break would happen

Source: WD-010; answer to Q-I1.

- Given a pull request in this repository or in any child repository
- When it is opened or updated
- Then the cross-repo checks run on it with the pull request's branch in place of that repository's main
- And they also run daily on main, and on demand

Test scenarios:
- T-WS-002a (anywhere, automated by GitHub Actions): a pull request in a child repository shows the cross-repo checks as a status. Today only this repository runs them.
- T-WS-002b (anywhere, manual once per repository): open a pull request in agent-e2 that changes one catalog limit; expect the KPI definitions check to fail on that pull request, before merge.

### R-WS-003 Every requirement is tested, and every test has a requirement

Source: ROADMAP M1; answer to Q-I1.

- Given the requirement files in [spec/requirements](.)
- When the specification check runs
- Then every requirement has a unique ID, a Source line that names an existing question or decision, and at least one test scenario
- And every test scenario belongs to an existing requirement and says where it runs (anywhere or lab)

Test scenarios:
- T-WS-003a (anywhere, automated by tools/spec_check.py): a requirement without a scenario, a scenario without a requirement, a duplicate ID or a Source that names no existing ID fails the check.

### R-WS-004 Documents work for people and for machines

Source: the author's message of 2026-11-25 on links and diagrams; WD-020.

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

Source: WD-020 (from Q-46).

- Given a document in this repository
- When it uses an ID such as C3, WD-012 or Q-27
- Then on its first use in that document it gives the meaning, or links to the [glossary](../glossary.md)

Test scenarios:
- T-WS-005a (anywhere, manual by a fresh reviewer for each pull request): read the changed files and list every ID used without its meaning. A check is not planned: the rule needs judgement about what a reader already knows.

### R-WS-006 One set of writing rules, checked in every repository

Source: WD-023 (writing rules for people and for machines), as revised for M2.

- Given the general writing rules (plain sentences, the flagged phrases, noun-phrase headings, short table cells) and the list of flagged phrases
- When any repository's documents for people are checked
- Then the rules and the list exist once, in this workspace
- And agent-e2's writing rules keep only what is particular to knowledge files, and link to the general ones
- And each repository runs [tools/style.py](../../tools/style.py) on its pull requests, against a baseline of its problems today that may only shrink

Test scenarios:
- T-WS-006a (anywhere, automated by tools/style.py in each repository's CI): a pull request that adds a flagged phrase or a sentence heading to a document for people fails; one that fixes a known problem passes and lowers the baseline.
- T-WS-006b (anywhere, automated by a check to write in agent-e2's lint): agent-e2's list of flagged phrases is read from this workspace; a copy of the list in agent-e2 fails.

### R-WS-007 Folder and file names carry no version, milestone or status word

Source: WD-030.

- Given the tracked folders and files of agent-e2, PCM-Adapter, private-cloud-manager, isvara and this workspace, outside archives and dated records
- When the name check runs
- Then no folder or file name contains a version (v2, v5), a milestone (m5) or a status word (proto, new, old, final, copy)
- And the problems found when the check is first written form a baseline that may only shrink

Test scenarios:
- T-WS-007a (anywhere, automated by a check to write in [checks](../../checks), run by run_all.py and in each repository's CI): a pull request that adds `report_v2.md` or `story_m5.py` fails; one that renames a known problem passes and lowers the baseline.
- T-WS-007b (anywhere, manual by a fresh session, once per repository): given only the repository's folder tree, the session writes what it expects in each top-level folder and in each folder one level down, then opens them. Each wrong guess becomes a rename in the same milestone.

## Questions for round two

- None.
