# CLAUDE.md

How the AI agent works on this project. Read at the start of every session.

## Start of every session

- Read SYSTEM.md, CONTRACTS.md, ROADMAP.md and the requirements the request touches. Name the milestone and the requirement IDs; if the request belongs to none, say so before starting.
- Read the CLAUDE.md of each repository the change touches.

## How to think

- A suggestion from the person is input to think with. Unless they say "decide" or "do it", reply first with what is strong, what is weak, what is missing, and a recommendation. Change the files only after you agree.
- Disagree when you have a reason.
- Decide what you can work out from the code, the documents or general knowledge of the field, and say what you decided. Ask only about judgement, experience, scope and taste.

## Specification first

- No build starts until its requirements and test scenarios are written and approved.
- Every requirement cites the answer or decision it comes from.

## Stop and ask when

- the specification does not decide something, or two documents disagree;
- a requirement cannot be tested as written;
- a fix would change a contract or reverse a decision;
- a test needs an environment you cannot reach (say so; never report it as passed).

Write the question in OPEN-QUESTIONS.md with a recommendation and an empty Answer line.

## Scope

- <What is in scope now; what is later and must not be built toward yet.>
- <Which part owns which facts.>

## Contracts and checks

- Run the checks before and after any change to a contract, and change a contract in three steps: add the new shape, move each consumer, remove the old shape.
- Never weaken, skip or delete a check or a test to make it pass. Record a known gap only together with an open question.

## Names

- Before adding an ID prefix, term, heading, folder or file name: make it guessable from itself, with one word per concept and no overlap with an existing one.
- Put no version, milestone or status word in a folder or file name.
- When a name or number stops being true: rename it in every file. Add no note that explains the exception.

## Session end

- Before reporting a session as finished: add its lessons to the case log.
- When work remains: write a prompt for the next session, with the files to read, the settled scope, the tasks and how to report.

## Git

- One branch and pull request per change per repository.
- <Who merges, when, and what counts as a major change that needs a warning.>
- Never merge before the checks have reported, or when they fail.

## Secrets

- <Where credentials live.> Never print, log or commit one.
