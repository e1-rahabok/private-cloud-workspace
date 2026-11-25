# Requirements: the isvara.io exam

The exam for people on isvara.io, roadmap milestone M7 ([ROADMAP.md](../../ROADMAP.md)). It has ten short, very hard multiple-choice questions that test depth of understanding. A wrong answer loses marks, and no answer scores 0. The exam is kept in isvara.io and is separate from Agent E2's benchmark, which tests the machine ([W-006](../../DECISIONS.md), a decision binding several repositories).

Question IDs (Q-) point at your answers in the [interview, round 1](../interview-round-1.md). Decision IDs (W-) are in [DECISIONS.md](../../DECISIONS.md). Other IDs are explained in the [glossary](../glossary.md). The rest of the site's revamp, including where the exam sits, is in [design/isvara-revamp.md](../design/isvara-revamp.md), feature 33.

Two words used below:

- **Exam data file:** the one file in the [isvara](https://github.com/e1-rahabok/isvara) repository that holds the questions, options, reasoning, marks and sources.
- **Export:** the files Agent E2 publishes for isvara.io to build pages from ([contract C4](../glossary.md#c4)). Each knowledge file in it has a content fingerprint that changes when the file changes.

### R-EXAM-001 The exam has its own page next to the 2am game

Source: W-006; answer to Q-56.

Given the site's header and home page
When a reader opens isvara.io
Then the header shows "Exam" beside "2am", and the home page has a link to `/exam`
And `/exam` opens the first question with no sign-in

Test scenarios:
- T-EXAM-001a (anywhere, automated by a page test in isvara, to write): open `/`; find a link to `/exam` next to the link to `/2am` in the header and on the home page; follow it; question 1 of 10 is shown.

### R-EXAM-002 Ten questions, each with one correct option

Source: W-006 ("10 short, very hard multiple-choice questions"); answer to Q-56 ("Format is MCQ").

Given the exam data file
When the site is built
Then the build accepts it only if it holds exactly 10 questions
And every question has the same number of options, with exactly one marked correct

Test scenarios:
- T-EXAM-002a (anywhere, automated by the exam data check in isvara, to write): a fixture with 9 questions fails the build; a fixture with a question that has two correct options fails; a fixture with a question that has no correct option fails; the real file passes.

### R-EXAM-003 A wrong answer loses marks and no answer scores 0

Source: W-006; answer to Q-56 ("Have a penalty for wrong answer. 0 for no answer").

Given the exam data file sets the mark for a correct answer and the penalty for a wrong one, both above 0
When a reader finishes the exam
Then each correct answer adds the mark, each wrong answer subtracts the penalty, and each unanswered question adds 0
And the result shows the total, the highest possible total, and how many answers were correct, wrong and unanswered
And the total is shown as it is, also when it is below 0

Test scenarios:
- T-EXAM-003a (anywhere, automated by a unit test of the scoring function, to write): with mark 3 and penalty 1:
  - all 10 correct scores 30;
  - all 10 wrong scores −10;
  - all 10 unanswered scores 0;
  - 5 correct, 2 wrong and 3 unanswered scores 13.
- T-EXAM-003b (anywhere, automated by a page test, to write): skip all 10 questions and finish; the result shows 0 of 30, with 0 correct, 0 wrong and 10 unanswered.

### R-EXAM-004 A reader may leave any question unanswered

Source: answer to Q-56 ("0 for no answer"); W-006.

Given any question on screen
When the reader chooses "Skip"
Then that question is locked as unanswered and its reasoning is shown
And the reader can go on to the next question

Test scenarios:
- T-EXAM-004a (anywhere, automated by a page test, to write): on question 4, choose Skip; the reasoning appears; no option can be chosen any more; Next opens question 5; the result counts question 4 as unanswered.

### R-EXAM-005 The reasoning is shown after each answer, and the answer is then locked

Source: W-006; answer to Q-56.

Given a question on screen
When the reader confirms an option
Then the correct option is marked, with why it is correct
And when the chosen option is wrong, why that option is wrong
And the reader's choice can no longer be changed

Test scenarios:
- T-EXAM-005a (anywhere, automated by a page test, to write): choose a wrong option on question 2 and confirm; the correct option and both explanations appear; clicking another option changes nothing; the result counts question 2 as wrong.
- T-EXAM-005b (anywhere, automated by a page test, to write): choose the correct option on question 3 and confirm; it is marked correct with its explanation.

### R-EXAM-006 The reasoning links to the topic pages it rests on

Source: W-017 ("a cited source opens the knowledge file"); answers to Q-45 and Q-I5.

Given a question's reasoning on screen
When the reader follows a source link in it
Then the topic page of that knowledge file opens
And every question lists at least one knowledge file

Test scenarios:
- T-EXAM-006a (anywhere, automated by the exam data check, to write): every knowledge file named by a question exists in the export and has a topic page; a fixture that names a missing file fails the build.
- T-EXAM-006b (anywhere, automated by a page test, to write): after answering question 1, follow its first source link; a topic page opens with the title of that file.

### R-EXAM-007 The exam is kept in isvara.io and calls no service

Source: answer to Q-56 ("Keep the exams at isvara.io"); W-006; W-014 (the US$50 a month limit on Vercel AI Gateway).

Given the site is built and served
When a reader takes and finishes the exam
Then the questions, options, reasoning and marks come only from the exam data file
And the page calls neither Agent E2 nor Vercel AI Gateway, nor any other service, to show or score the exam
And the reader's answers leave the browser only as one anonymous usage count on finishing

Test scenarios:
- T-EXAM-007a (anywhere, automated by a page test that records network requests, to write): take the whole exam; the only request made after the page loads is the usage count, and it carries no answer.
- T-EXAM-007b (anywhere, automated by the exam data check, to write): change one question's text in the data file and build; the new text appears on `/exam`.

### R-EXAM-008 Each question stays aligned with Agent E2's knowledge

Source: W-001 ("isvara.io holds no knowledge of its own"); answers to Q-18 and Q-56.

Given each question lists the knowledge files it rests on, with each file's content fingerprint from the export at the time the question was checked
When the site is built with a newer export
Then the build fails if a listed file has changed or no longer exists, and names the question and the file
And it passes again only after the question has been checked against the new file and its fingerprints updated

Test scenarios:
- T-EXAM-008a (anywhere, automated by the exam data check, to write): with a fixture export where one cited file's fingerprint differs, the build fails and names that question and file.
- T-EXAM-008b (anywhere, automated by the exam data check, to write): with a fixture export where a cited file is missing, the build fails.
- T-EXAM-008c (anywhere, automated by the exam data check, to write): with an export where every cited file is unchanged, the build passes.

### R-EXAM-009 Every answer and its reasoning are supported by the knowledge files

Source: W-013 (free-text answers are graded automatically by a strong model as judge); answer to Q-5; W-001.

Given a question, its options, its reasoning and the text of the knowledge files it lists
When the judge checks it
Then the judge confirms that the correct option is correct according to the files, and each other option is wrong according to them
And it confirms that the reasoning makes no claim the files do not support
And a question the judge rejects is not published

Test scenarios:
- T-EXAM-009a (anywhere, automated by the exam battery with the judge model, to write; needs the gateway key): the 10 published questions all pass.
- T-EXAM-009b (anywhere, automated by the same battery, to write): a fixture question whose marked option contradicts its file is rejected.

### R-EXAM-010 Questions test a mechanism and need no calculation

Source: W-006 ("test depth of understanding, not calculation").

Given a question
When the judge checks it
Then answering it needs no arithmetic
And it asks about how something works, or about a reading that misleads, as its knowledge files explain it

Test scenarios:
- T-EXAM-010a (anywhere, automated by the exam battery with the judge model, to write; needs the gateway key): each of the 10 questions is classed as answerable without calculation and as testing a mechanism or a misleading reading; a fixture question that asks for a computed value is rejected.

### R-EXAM-011 Questions and options are short

Source: W-006 ("10 short, very hard multiple-choice questions").

Given the exam data file
When the site is built
Then each question's text is at most 50 words and each option at most 20 words (limits to confirm in round two, Q-117 in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md))

Test scenarios:
- T-EXAM-011a (anywhere, automated by the exam data check, to write): a fixture question of 51 words fails the build; a fixture option of 21 words fails; the real file passes.

### R-EXAM-012 The exam is separate from Agent E2's benchmark

Source: W-006 ("separate from Agent E2's benchmark"); W-021.

Given the exam questions and the questions in Agent E2's [benchmark](https://github.com/e1-rahabok/agent-e2/tree/main/benchmark), where any remain
When the exam check runs
Then no exam question shares a run of 12 or more words with a benchmark question

Test scenarios:
- T-EXAM-012a (anywhere, automated by the exam data check reading the agent-e2 clone, to write): a fixture question copied from a benchmark question fails; the real file passes.

### R-EXAM-013 The exam keeps the site's look and works on a phone

Source: W-017 ("same look and feel"); answer to Q-44.

Given the dark and the light theme, and a screen 375 pixels wide or a desktop screen
When `/exam` opens and a question is answered
Then the page uses the site's design in both themes
And on the narrow screen it needs no sideways scrolling

Test scenarios:
- T-EXAM-013a (anywhere, automated by a page test with screenshots, to write): open `/exam` at 375 pixels and at desktop width, in both themes; the page is no wider than the screen; the screenshots are kept for review.

## Questions for round two

The questions on this file are in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md), Q-109 to Q-118, each with a recommendation and an Answer line.
