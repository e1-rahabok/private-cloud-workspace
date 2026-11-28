# Design

How the parts meet the requirements within the constraints, and why this way. The agent writes it as the architect. The person reads it to learn and to catch a mistake about the domain. Current state only; git keeps the history.

## Context

- Goals: <GOAL IDs from BRIEF.md>
- Constraints: <CONSTRAINT IDs>
- Requirements: <the requirement files>

## Structure

| Part | Repository | Runs where | Talks to |
|---|---|---|---|
| | | | |

## Where each kind of thing comes from

| Thing | Master copy | Used by |
|---|---|---|
| | | |

## Environments

| Host or service | What | Access, and where its secret lives |
|---|---|---|
| | | |

Never write a secret here; name the file or vault that holds it.

## Build and test per repository

| Repository | Runs anywhere | Needs a special environment |
|---|---|---|
| | | |
| All together | `<command that runs the cross-repo checks>` | |

## Contracts

| ID | Contract | Owner, then consumers | Check |
|---|---|---|---|
| C1 | | | <running, planned in milestone, or none with the reason> |

### C1 <name>

- Owner: <repository and file that define the shape>
- Consumers: <repository and file that depend on it>
- The check: <what it compares or calls, and how it fails>

A contract changes in three steps, and the checks pass after each: the owner adds the new shape and keeps the old one working; each consumer moves to the new shape; the owner removes the old shape.

## Quality attributes

| Attribute | Target | Mechanisms |
|---|---|---|
| Security | <requirement ID, or the threat to block> | <DESIGN IDs> |
| Scalability | <the size to reach, in numbers> | |
| Performance | <requirement ID with its number> | |
| Reliability | <what must never look healthy when it is not> | |
| Maintainability | <where each definition lives> | |
| Testability | <the data with known answers> | |
| Cost | <the budget, CONSTRAINT ID> | |

## Choices

### DESIGN-1 <the choice, in a few words>

- Context: <the problem, and the constraints that bear on it>
- Options: <a>, <b>, <c>
- Choice: <the option taken>
- Reasons: <why it wins, and why each other option loses>
- Consequences: <what it costs, and what it rules out>
- Serves: <GOAL, CONSTRAINT and R- IDs>
- Proven by: <T- IDs or a check>

## Deferred

- <A choice that waits: what it waits for, and the rule it will follow.>
