# Contracts

Every interface between two parts. Each has one owner, its consumers, where its shape is written, and the check that proves both sides agree.

| ID | Contract | Owner | Consumers | Check | Status |
|---|---|---|---|---|---|
| C1 | | | | | Running / planned (milestone) / none (reason) |

## C1 <name>

- **Owner:** <repository and file that define the shape>
- **Consumers:** <repository and file that depend on it>
- **The check:** <what it compares or calls, and how it fails>

## Changing a contract

1. **Expand:** the owner adds the new shape and keeps the old one working.
2. **Migrate:** each consumer moves to the new shape.
3. **Contract:** the owner removes the old shape.

The checks pass after every step.
