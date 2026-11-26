# 8. Slices and sessions

## Slices

Build in thin slices. A slice goes end to end through every part it touches but covers only a narrow case, for example one cluster and one score, rather than all of them. After each slice the whole system still works and every check passes.

Order the slices by how much is unknown, and start with the most. In this project, connecting the web app to the live lab came early: the API had never been called against a live instance, the metric keys had never been read for real, and nobody knew whether the web app's server could reach the lab at all. Whatever that slice teaches changes the later ones. Extending the same pattern to more scores has few unknowns, so it comes after.

Finishing one repository before starting the next sounds tidy, but it pushes every problem between repositories to the end, where it is most expensive to fix.

## Sessions

Work in one long session per slice, rather than many small ones. Each session follows the same shape:

1. The agent reads the map, the contracts, the roadmap and the requirements, and the working rules of each repository the slice touches.
2. It names the milestone and the requirement IDs it is working on. If the request belongs to none, it says so before starting.
3. It lists anything the requirements leave open, and the person answers. Questions that can wait go into the open questions file.
4. It builds, runs every check with the changed branches in place, and runs each repository's own tests.
5. When something is not decided, it writes the question with a recommendation and stops that line of work.
6. At the end it marks the finished requirements in the roadmap with their pull request, and writes corrections back into the map and the decisions.

## When the agent must stop

These go into [CLAUDE.md](../CLAUDE.md), so every session follows them:

- the specification does not decide something, or two documents disagree;
- a requirement cannot be tested as written;
- a fix would change a contract or reverse a decision;
- a test needs the lab and the lab cannot be reached, in which case it says so and never reports the test as passed;
- the work would delete data or change a live system.

## Git

- One branch and one pull request per change, per repository.
- A change across repositories uses the same branch name in each, and the pull requests link to each other.
- Merge in order of ownership: the owner of a contract first, then the parts that depend on it.

Who merges depends on the stage of the project. Early on, while most changes are scope and documentation, the agent merges its own pull requests once the checks pass, and warns the person when a change is major: a contract changes, a decision is added or reversed, files are deleted, or several repositories change together. Waiting for a review of every documentation change would cost more than it saves. Once the product has users, routine work still merges on passing checks, but contract changes and new decisions wait for a person.

The checks are what make the early rule safe. Without them, merging unreviewed work is a gamble. With them, the person can read the warnings and the roadmap instead of every change.

One more lesson from this project: wait for the checks to actually report before merging. Once, the command that waits for them returned before the checks had even started, and the merge went through unchecked. The checks passed afterwards, but that was luck.

## Exercise

List your goals and order them by how much is unknown. Which one would teach you the most if you built a thin version of it first?
