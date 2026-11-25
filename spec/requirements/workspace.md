# Requirements: the workspace

What keeps the four repositories one integrated set: the contract checks, the specification's own checks, and the documentation rules. Question IDs (Q-) point at the author's answers in the [interview, round 1](../interview-round-1.md); other IDs are explained in the [glossary](../glossary.md).

### R-WS-001 Every contract has an automated check

Source: answer to Q-I1 ("I expect you to check all the contracts"); W-010.

Given a contract listed in [CONTRACTS.md](../../CONTRACTS.md)
When the checks run
Then the contract has a check that fails when its two sides disagree
And each check has been shown to fail on a planted break

Test scenarios:
- T-WS-001a (anywhere, automated by tools/spec_check.py, to extend): every row of CONTRACTS.md names an existing check file, or is marked planned with a milestone.
- T-WS-001b (anywhere, manual once per check): plant a break, run the check, record the failure in the check's docstring.

### R-WS-002 The checks run where a break would happen

Source: W-010; answer to Q-I1.

Given a pull request in this repository or in any child repository
When it is opened or updated
Then the cross-repo checks run on it with the pull request's branch in place of that repository's main
And they also run daily on main, and on demand

Test scenarios:
- T-WS-002a (anywhere, automated by GitHub Actions): a pull request in a child repository shows the cross-repo checks as a status. Today only this repository runs them.

### R-WS-003 Every requirement is tested, and every test has a requirement

Source: ROADMAP M1; answer to Q-I1.

Given the requirement files in [spec/requirements](.)
When the specification check runs
Then every requirement has a unique ID, a Source line that names an existing question or decision, and at least one test scenario
And every test scenario belongs to an existing requirement and says where it runs (anywhere or lab)

Test scenarios:
- T-WS-003a (anywhere, automated by tools/spec_check.py): a requirement without a scenario, a scenario without a requirement, a duplicate ID or a Source that names no existing ID fails the check.

### R-WS-004 Documents work for people and for machines

Source: the author's message of 2026-11-25 on links and diagrams; W-020.

Given any Markdown file in this repository
When the documentation check runs
Then every file reference is a clickable link
And every diagram is an SVG drawn by a script, with its text generated underneath
And every relative link resolves

Test scenarios:
- T-WS-004a (anywhere, automated by tools/docs.py --check and tools/diagrams.py in CI): an unlinked path, a stale diagram text or a broken link fails.

### R-WS-005 No bare short names

Source: W-020 (from Q-46).

Given a document in this repository
When it uses an ID such as C3, W-012 or Q-27
Then on its first use in that document it gives the meaning, or links to the [glossary](../glossary.md)

Test scenarios:
- T-WS-005a (anywhere, manual by a fresh reviewer for each pull request): read the changed files and list every ID used without its meaning. A check is not planned: the rule needs judgement about what a reader already knows.

## Questions for round two

- None.
