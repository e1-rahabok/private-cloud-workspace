# 7. Slices and sessions

## Slices

Build in thin slices. A slice goes end to end across every part it touches, but covers only a narrow case: one cluster and one KPI, not all of them. After each slice the whole system works and the checks pass.

**Riskiest first.** Order the slices by how much is unknown. In this workspace, connecting the web app to a live system came early (M2): the APIs had never been tried against a live instance, the metric keys had never been read for real, and the network path from the app's server to the live system was unproven. Everything learned there changes the later slices. A slice with few unknowns, such as extending the same pattern to more KPIs (M3), comes after.

**Why not one repository at a time?** "Finish repository A, then B" defers every seam problem to the end, when it is most expensive.

## Sessions

One long session per slice, not hundreds of small ones. A session follows the same shape each time:

1. **Read.** The agent reads the map, the contracts, the roadmap, and the CLAUDE.md of each repository the slice touches.
2. **Confirm the slice.** The agent names the milestone and its definition of done. If the request fits none, it says so before starting.
3. **Ask before building.** The agent lists what the specification does not decide, and the human answers. Questions that can wait go to OPEN-QUESTIONS.
4. **Build and check.** The agent builds, runs the checks with the changed branches, and runs each repository's own tests.
5. **Stop when stuck.** When something is not decided, it writes the question with a recommendation and stops that line of work. It does not guess.
6. **Write back.** Finished lines are marked in the roadmap with their pull request. Corrections go into the map and the decisions.

## Stop conditions

Write them into `CLAUDE.md`, so every session follows them:

- The specification does not decide something.
- A check fails and the fix would mean changing a contract.
- A test needs the lab and the lab is not reachable: say so plainly, do not claim it passed.
- The work would delete data or change a live system.

## Git

- One branch and pull request per change per repository.
- A change across repositories uses the same branch name in each, and the pull requests link each other.
- Merge in order of ownership: the owner of a contract first, then its consumers.
- Who merges depends on the phase of the project.

**Early phase** (this workspace today): most changes are scope and documentation. The agent merges every pull request once the checks pass, and warns the human when a change is major: a contract changes shape, a decision is added or reversed, files are deleted, or several repositories change together. Waiting for review would cost more than it saves.

**Later phase** (the product has users): routine work still merges on green checks, but a contract change or a new cross-repo decision waits for a human review.

The checks are what make the early-phase rule safe. Without them, merging without review is a gamble; with them, the human reads the warnings and the roadmap instead of every diff.

## Exercise

Take your goals and order them by unknowns. Which one would teach you the most if you built a thin version first?
