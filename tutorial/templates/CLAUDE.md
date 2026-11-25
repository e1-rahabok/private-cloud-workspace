# CLAUDE.md

How the AI agent works on this project. Read at the start of every session.

## Start of every session

- Read SYSTEM.md, CONTRACTS.md and ROADMAP.md. Name the milestone the request belongs to; if none, say so before starting.
- Read the CLAUDE.md of each repository the change touches.

## Scope

- <What is in scope now; what is later and must not be built toward yet.>
- <Which part owns which facts.>

## Contracts and checks

- Run the cross-repo checks before and after any change to a contract.
- Change a contract by expand, migrate, contract.
- Never weaken a check to make it pass. A known gap goes in a baseline only with an entry in OPEN-QUESTIONS.md.

## Decisions and questions

- When the specification does not decide something, stop and write the question to OPEN-QUESTIONS.md with a recommendation. Do not guess.
- Record cross-repo decisions in DECISIONS.md. Mark finished roadmap lines with the pull request.

## Git

- One branch and pull request per change per repository.
- <Who merges, when, and what counts as a major change that needs a warning.>
- Never merge with failing checks.

## Secrets

- <Where credentials live.> Never print, log or commit one.
