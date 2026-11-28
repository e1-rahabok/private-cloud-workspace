# 12. Slices and sessions

## Slices

Build in thin slices. A slice goes end to end through every part it touches but covers only a narrow case, for example one cluster and one score, rather than all of them. After each slice the whole system still works and every check passes.

Order the slices by how much is unknown, and start with the most. In this project, connecting the web app to the live lab held the most unknowns: the API had never been called against a live instance, the metric keys had never been read for real, and nobody knew whether the web app's server could reach the lab at all. Whatever that slice teaches changes the later ones. Extending the same pattern to more scores has few unknowns, so it comes after.

Where the work can run limits the order too. The lab sits behind a VPN that only the author's laptop reaches, and the agent's cloud sessions cannot. Spread over three milestones, the lab tests would have held each of them open until the author had time for a lab session. The author chose to gather every lab test into the live demo's milestone and put it last, accepting that its unknowns surface later. Its first slice is still one cluster and one score.

Finishing one repository before starting the next sounds tidy, but it pushes every problem between repositories to the end, where it is most expensive to fix.

## Sessions

Work in one long session per slice, rather than many small ones. Each session follows the same shape:

1. The agent reads the map, the contracts, the roadmap and the requirements, and the working rules of each repository the slice touches.
2. It names the milestone and the requirement IDs it is working on. If the request belongs to none, it says so before starting.
3. It lists anything the requirements leave open, and the person answers. Questions that can wait go into the open questions file.
4. It builds, runs every check with the changed branches in place, and runs each repository's own tests.
5. When the specification leaves open something only the person can supply, it writes a question that asks for that input, with the assumption it works on meanwhile, and stops that line of work.
6. At the end it marks the finished requirements in the roadmap with their pull request, and writes corrections back into the brief, the requirements and the design.
7. It adds the session's lessons to the case log and to the chapter of the method each belongs to. In this project the agent forgot this until the author asked, so it is now a written rule.
8. When work remains, it writes a prompt the person can paste into the next session: the files to read, the scope already settled, the tasks, and how to report.

Before asking the person to approve the next milestone, the agent checks that every other item of the current one is done. In this project the agent once asked for approval of M2 while four items of M1 were open, any of which could still change M2.

## Stop conditions

These go into [CLAUDE.md](../CLAUDE.md), so every session follows them:

- the specification does not decide something, or two documents disagree;
- a requirement cannot be tested as written;
- a fix would change a contract's shape or reverse a design choice or requirement;
- a test needs the lab and the lab cannot be reached, in which case it says so and never reports the test as passed;
- the work would delete data or change a live system.

## Git

- One branch and one pull request per change, per repository.
- A change across repositories uses the same branch name in each, and the pull requests link to each other.
- Merge in order of ownership: the owner of a contract first, then the parts that depend on it.

Who merges depends on the stage of the project. Early on, while most changes are scope and documentation, the agent merges its own pull requests once the checks pass, and warns the person when a change is major: a contract's shape changes, a design choice or requirement is reversed, files are deleted, or several repositories change together. Waiting for a review of every documentation change would cost more than it saves. Once the product has users, routine work still merges on passing checks, and a change to a contract's shape waits for a person's review.

The checks are what make the early rule safe. Without them, merging unreviewed work is a gamble. With them, the person can read the warnings and the roadmap instead of every change.

A conversation that settles several questions in a row produces several pull requests that touch the same files, such as the roadmap. Opened side by side, they conflict. Build each one on top of the one before it instead. Merging the last one then merges the whole stack.

What a requirement cites goes in before the requirement. The specification check refuses a requirement whose source names an ID that does not exist yet, and each repository's CI reads those IDs from the parent's main branch. So when the author answered six questions on one day, the parent recorded the answers in a pull request of its own and merged it first. Then each child repository's pull request could cite them.

A check that runs in one repository only sets the order too. The check that every repository holds the same [CLAUDE.md](../CLAUDE.md) runs in the workspace's CI and compares the workspace's copy with each child's main branch. When the method changed on 2026-11-28, the new CLAUDE.md went into the four children first, where nothing compares it, and into the workspace last, whose pull request then found all five copies equal. In the other order, the workspace's pull request would have failed until every child had caught up.

One more lesson from this project: wait for the checks to actually report before merging. Once, the command that waits for them returned before the checks had even started, and the merge went through unchecked. The checks passed afterwards, but that was luck.

## Exercise

List your goals and order them by how much is unknown. Which one would teach you the most if you built a thin version of it first?
