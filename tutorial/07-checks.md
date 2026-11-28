# 7. Checks

## Purpose

A check is a short script that reads two sides of a seam and fails when they disagree. It runs on every pull request, once a day, and whenever someone asks. The checks in this project are in [checks](../checks) and [tools](../tools), and each can be read in a few minutes.

## Two kinds

The first kind compares definitions. [checks/kpi_definitions.py](../checks/kpi_definitions.py) reads the performance definitions in the knowledge service's catalog and in the management pack's code, and compares them row by row, 49 sub-metrics in all: it finds each row by its key, then compares the name, the five limits, one flag and the interval, and also the score bands and the closure levels. It connects to nothing and runs in about a second.

The second kind exercises the real thing. [checks/agent_e2_api.py](../checks/agent_e2_api.py) starts the actual knowledge service with its model switched off, then calls each endpoint using the web app's own client code and checks every field the web app reads. It takes about eight seconds. Because it uses the real code on both sides, it catches a change that a comparison of documents would miss.

Use the second kind where it is cheap enough. Documentation can say one thing while the code has already moved on.

## Make sure a check can fail

After writing a check, break something on purpose and run it. In this project a limit in the catalog was changed from 200 to 250, and the first check failed and named the row. A field in the service's response was renamed, and the second check failed and named the field. Then the changes were undone. It takes ten minutes, and without it you do not know whether the check works at all.

Plant the break on a copy of the file and restore it from the copy. In this project the agent once planned to undo a planted break with `git checkout` on the roadmap, which would also have thrown away its own edits that were not yet committed. The session's permission check refused the command.

## Known gaps

A new check often finds real problems that cannot all be fixed at once. The first check here found 11 sub-metrics whose names differed between the two repositories, although their limits agreed. Letting the check fail every day until all 11 were fixed would have taught everyone to ignore it. Removing it would have let the gaps grow.

Instead the 11 were listed in the check as known gaps. They were reported, but they did not fail the run. Any new gap did fail, and so did a listed gap that had since been fixed, until someone removed it from the list. The list could only get shorter, and in M2 it reached zero. Each known gap has an open question that names who decides the fix. The one gap left, the Cluster Risk closure level, waits for the author's answer to [Q-WS-138](../OPEN-QUESTIONS.md).

## Checks on the specification itself

The same idea applies to the documents. One script fails when a requirement has no source or no test scenario, or a scenario belongs to no requirement. Another fails when a file reference is not a clickable link, or when a diagram's text no longer matches its picture. A third checks the writing of every document meant for people against the author's writing rules ([tools](../tools); [chapter 9](09-working-with-the-agent.md)).

The plan itself is checked too. When the roadmap was rebuilt, a count showed that 26 of the 32 requirements of the live demo belonged to no milestone and two belonged to two. Nobody had noticed, because each milestone read well on its own. The review tool now fails when a requirement sits in no milestone or in two, and when a test that needs the lab sits in a milestone that does not run there; the milestone gate fails when two milestones own one file, or when the numbers do not run M1, M2, M3.

## Places they run

- Locally, with one command: `uv run checks/run_all.py`.
- In GitHub Actions, on every push and pull request to this repository, once a day, and on demand.
- On every pull request in each of the other repositories, through one shared workflow each of them calls, so a break is caught before it merges rather than the next morning.

## Rules for the agent

- Never weaken, skip or delete a check or a test to make it pass.
- Add a known gap only together with an open question about it.
- Every new seam gets a check, or a line in the roadmap saying when it will.

## Exercise

Pick one seam from chapter 5's exercise. Write a script that reads both sides and compares one thing. Break one side on purpose. Did the script fail?
