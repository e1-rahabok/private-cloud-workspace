# Teaching guide

For anyone using this tutorial in a workshop or a course.

## Learning outcomes

1. Explain when iterative prompting is enough and when a specification pays for itself.
2. Divide the work: name what the domain expert gives as input and what the agent decides as architect.
3. Write a one-page map of a system that keeps what exists now apart from what is planned.
4. Write goals as measurable outcomes, with a scope that says what is out and why.
5. Run an interview that asks the person for input, and tell an input question from a design question or one the agent should answer itself.
6. Sort statements into constraints, assumptions, risks and dependencies, and handle each the right way.
7. Write a requirement in Given, When, Then form, with a source, a reason, acceptance criteria and a test scenario, including a failure case.
8. Write a design choice with its context, options, reasons and consequences, and name the quality attribute it serves.
9. List the seams of a system and name an owner for each.
10. Write a test plan with levels, environments and data, and trace one requirement from its goal to its test.
11. Write a check for one seam and show that it fails when something breaks.
12. Name files, folders, IDs and terms so a new session can guess what they hold.
13. Start a first project of their own with one seam.

## Format: two days, or six sessions of 90 minutes

1. **The problem, the method and the map** (chapters 1 to 3). Participants ask an agent to describe a sample repository, then count its mistakes and find the documents that caused them.
2. **Goals, the interview and the conditions** (chapters 4 to 6). Participants write a goal with a measure. The agent surveys the sample for open questions; participants sort them into input questions, design questions and questions the agent should have answered itself, then sort a list of statements into constraints, assumptions, risks and dependencies.
3. **Requirements and design** (chapters 7 to 9). Turn a vague goal into requirements with reasons and acceptance criteria. The agent writes two design options for one of them; participants judge its reasons and pick out the constraint that decides. Draw the seams and name their owners.
4. **Test plan and checks** (chapters 10 and 11). Write a test plan for the sample, trace one requirement from goal to test, write a small check, and break something on purpose.
5. **Running the work** (chapters 12 to 14). Run one slice with an agent, following the session shape. Give the agent a suggestion and see whether it argues or obeys. Show the agent only a folder tree and count its wrong guesses. Review the result in a fresh session.
6. **Trust, the case study and a first project** (chapters 15 to 17). Walk through one day of the case log. Each participant picks a first project with one seam and writes its brief before the session ends.

## Video calls

For a series of video calls, one call per session above:

- Share the repository in the browser. Open the real files as each chapter names them; the links in every chapter go straight to them.
- Spend about 30 minutes explaining, 40 minutes on a live demonstration with an agent on a small sample repository, and 20 minutes on questions.
- Run the demonstration on a sample with nothing sensitive in it. Close other windows; never show a credential on screen.
- Give the chapter's exercise as homework, and open the next call with two or three participants' results.
- Record the calls. The chapters and the recording together let a participant who missed a call catch up alone.

## Materials

- This repository and its [checks](../checks) and [tools](../tools) as the worked example.
- The [templates](templates) for participants' own projects.
- Any small project with two parts that share something, such as a web app and its API, or a script and the file format it reads. Two repositories of a few dozen files each are enough.

## Discussion questions

- When is iterative prompting the better choice? Where exactly does it stop being enough?
- The agent's first survey was wrong in four places. Was that a failure of the agent or of the documentation?
- The author said where the knowledge belongs; the agent designed the master copy and its check. Where is the line between the expert's input and the architect's decision?
- WD-015 holds five kinds of statement in one paragraph ([chapter 2](02-the-method.md)). Sort them. What happens to each kind when it sits in a decision log?
- Q-WS-136 asked the author to choose one of three designs for a security guard. Which input did the choice really need, and who should have made it?
- Agent E2 and isvara.io answered questions about the same books with opposite designs. Which constraint decided each one?
- A check found 11 known gaps on its first run. Fail every build until they are fixed, or record them as known? What can go wrong with each?
- The author found a wrong fact about the books' source in a README, and the agent fixed the sentence. What did that fix leave wrong, and what would the architect's step have found first?
- The agent turned a suggestion into a decision within an hour. What in the working rules, and what in the way answers were recorded, let it happen?
- The strongest model available made every mistake in the case study. What does that say about choosing models?
- A calculator with no AI in it can still be wrong. How would you prove a calculator is right?
- In the case study the plan grew to 43 requirements the author never meant to include, each with a good source. How would you have caught it earlier?
- The agent chose a product's name when asked to, and the author reversed it. Which inputs should a person keep giving even when delegating?
- Which of the VMware tasks in the README's table do you already do well? Which step of the method would be easiest for you?

## Assessment

For a project of their own, each participant hands in:

- a brief: one goal with its measure, the scope with one item out and its reason, and two constraints, two assumptions and one risk;
- ten interview questions, each asking for input and stating the working assumption;
- three requirements with reasons, acceptance criteria and scenarios, one of them about a failure;
- one design choice with two rejected options, and the quality attribute it serves;
- a contract table with at least three seams and their owners;
- a test plan of one page, with one requirement traced from goal to test;
- one check, with evidence that it failed when something was broken;
- a glossary of the ten terms their project uses most, one meaning each.

## Notes for the teacher

- The subject matter of the case study does not matter. Point participants at the shape of the files, not their content.
- The most common mistake is describing the plan as if it already existed. Look for it in every map.
- The second is a check that cannot fail. Always ask to see it fail.
- The third is an interview full of questions the agent could have answered. Ask participants to cut those first.
- The fourth is a question that asks the person to pick a design. Ask what input the design needs, and let the agent decide.
- Domain experts tend to under-specify the quality attributes. Ask for one number each: how fast, how many, how much it may cost.
