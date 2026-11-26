# Teaching guide

For anyone using this tutorial in a workshop or a course.

## What participants should be able to do afterwards

1. Explain when iterative prompting is enough and when a specification pays for itself.
2. Write a one-page map of a system that keeps what exists now apart from what is planned.
3. Run an interview: have an agent list the open questions in a repository, each with a recommendation, and tell a judgement question from one the agent should answer itself.
4. List the seams of a system and name an owner for each.
5. Write a requirement in Given, When, Then form, with a source and a test scenario, including a failure case.
6. Write a check for one seam and show that it fails when something breaks.
7. Reply to an agent's suggestion as a co-architect: what is strong, what is weak, and a recommendation.

## Format: one day, or four sessions of 90 minutes

| Session | Chapters | Activity |
|---|---|---|
| 1. Why, and the map | 1, 2, 3 | Participants ask an agent to describe a sample repository, then count its mistakes and find the documents that caused them |
| 2. Interview, seams and owners | 4, 5 | The agent surveys the sample for open questions; participants sort them into judgement questions and questions the agent should have answered itself; then draw the seams and choose owners |
| 3. Requirements and checks | 6, 7 | Turn a vague goal into requirements with scenarios; write a small check; break something on purpose |
| 4. Running the work | 8, 9, 10, 11 | Run one slice with an agent, following the session shape; give the agent a suggestion and see whether it argues or obeys; review the result in a fresh session |

## Materials

- This repository and its [checks](../checks) and [tools](../tools) as the worked example.
- The [templates](templates) for participants' own projects.
- Any small project with two parts that share something, such as a web app and its API, or a script and the file format it reads. Two repositories of a few dozen files each are enough.

## Discussion questions

- When is iterative prompting the better choice? Where exactly does it stop being enough?
- The agent's first survey was wrong in four places. Was that a failure of the agent or of the documentation?
- Why should the person, and not the agent, decide which copy of a shared fact is the master?
- A check found 11 known gaps on its first run. Fail every build until they are fixed, or record them as known? What can go wrong with each?
- The agent turned a suggestion into a decision within an hour. What in the working rules would have stopped it?
- The strongest model available made every mistake in the case study. What does that say about choosing models?
- A calculator with no AI in it can still be wrong. How would you prove a calculator is right?

## Assessment

For a project of their own, each participant hands in:

- a one-page map;
- ten interview questions, each with a recommendation;
- a contract table with at least three seams and their owners;
- three requirements with scenarios, one of them about a failure;
- one check, with evidence that it failed when something was broken.

## Notes for the teacher

- The subject matter of the case study does not matter. Point participants at the shape of the files, not their content.
- The most common mistake is describing the plan as if it already existed. Look for it in every map.
- The second is a check that cannot fail. Always ask to see it fail.
- The third is an interview full of questions the agent could have answered. Ask participants to cut those first.
