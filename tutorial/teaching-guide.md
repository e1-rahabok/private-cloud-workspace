# Teaching guide

For a teacher who wants to use this tutorial in a workshop or a course.

## Learning outcomes

After the workshop, a participant can:

1. Explain why many small AI conversations drift, with two causes.
2. Write a one-page map of a system that keeps the current state apart from the target.
3. List the seams of a system and name an owner for each.
4. Turn a goal into five checkable statements.
5. Write a check for one seam and prove it can fail.
6. Run an AI session that reads the files, asks before it guesses, and writes back what it learned.

## Format: one day, or four sessions of 90 minutes

| Session | Chapters | Activity |
|---|---|---|
| 1. The problem and the map | 1, 2, 3 | Participants ask an AI agent to describe a sample repository, then count and explain its mistakes |
| 2. Seams and owners | 4 | Draw the parts and lines of a sample system; find a fact held in two places; decide its owner |
| 3. Done and checks | 5, 6 | Rewrite a vague goal as a definition of done; write a small check; plant a break |
| 4. Running the work | 7, 8, 9 | Run one slice with an AI agent, following the session shape; review it in a fresh session |

## Materials

- This repository and its [checks](../checks) as the worked example.
- The [templates](templates) for participants' own projects.
- Any small project with two parts that share something: a web app and its API, a script and the file format it reads. Two repositories of a few dozen files each are enough.

## Discussion questions

- When is a longer prompt the right answer, and when is it not?
- In the case study, the AI's first survey was wrong in four places. Was that a failure of the AI or of the documentation?
- Why should the human decide which copy of a fact is the master, rather than the agent?
- A check found 11 known gaps on its first run. Fail the build until they are fixed, or record a baseline? What are the risks of each?
- Which decisions should wait for a human, and which can the agent merge on its own?

## Assessment

Ask each participant to hand in, for a project of their own:

- a one-page map;
- a contract table with at least three seams and their owners;
- one goal written as a definition of done;
- one check, with evidence that it failed on a planted break.

## Notes for the teacher

- The domain of the case study (VMware operations) does not matter. Point participants to the structure of the files, not their content.
- The most common mistake is writing the target state as if it were the present. Look for it in every map.
- The second most common mistake is a check that cannot fail. Always ask for the planted break.
