# 13. Your first project

A plan for a VMware administrator who has read this tutorial and wants to try the method on their own work. It takes about a week of evenings. The example is invented for this chapter; swap in your own.

## Tools

- A GitHub account, and one private repository for the project.
- An AI coding agent that can read and change files in that repository, such as Claude Code.
- A test environment you may break: a homelab, a nested lab, or a read-only account on a non-production vCenter or VCF Operations. Never give the agent an administrator credential to production.

## A project with one seam

Pick something small that has two parts sharing one thing. Two parts are enough to learn every step, because the shared thing is your first seam. Ideas from an administrator's week:

| Part one | Part two | The seam |
|---|---|---|
| A PowerCLI script that exports VM inventory to CSV | A spreadsheet or dashboard that reads the CSV | The column names, units and order |
| A capacity report script | The threshold sheet it reads | Each threshold's name and value |
| An alert definition in VCF Operations | The runbook the on-call engineer follows | The alert's name and what triggers it |

The rest of this chapter uses the first row: an inventory script and the dashboard that reads its CSV.

## Day 1: the map

- Copy the [templates](templates) into the repository.
- Ask the agent to read the script and the dashboard, and fill in SYSTEM.md and CONTRACTS.md. The prompt is in the [templates README](templates/README.md).
- Read its draft. Count what it got wrong, and fix the documents (chapter 3). Typical mistakes: it describes what you plan as if it already exists, or it misses that the dashboard expects memory in GB while the script writes MB.

## Day 2: the interview

- Ask the agent to list conflicts, undecided items, unstated assumptions and missing requirements, each with a recommendation (chapter 4).
- Answer them in OPEN-QUESTIONS.md, in a word where you can. Expect questions such as: what happens to a VM that is powered off? Does a template count as a VM?
- Cross out every question the agent could have answered from the code or from general VMware knowledge. Tell it so; the next round will be shorter.

## Day 3: the seam and its owner

- Write the CSV's columns down as a contract: owner, consumer, shape (chapter 5).
- Decide the master: the script defines the columns, and the dashboard follows. Write it in DECISIONS.md with one sentence of reason.

## Day 4: requirements

- Write three requirements in Given, When, Then form, each with a test scenario (chapter 6). Make one of them a failure case, for example: a vCenter that cannot be reached is listed in the CSV with an error, and its VMs are never left out silently.
- Give each one a source: the question or decision it came from.

## Day 5: the check

- Ask the agent for a script that reads the script's column list and the dashboard's expected columns, and fails when they differ (chapter 7).
- Rename one column on purpose. The check must fail. Undo it.

## Day 6 and later: one slice at a time

- Write ROADMAP.md with the first slice: one vCenter, three columns, end to end (chapter 8).
- Start each session with the agent reading the files and naming the requirement it works on.
- End each session by writing what you learned into a short case log, as [chapter 12](12-case-study.md) does for this project.

## Signs that it works

- A new session starts work without you explaining the system again.
- The agent asks you fewer questions each round, and better ones.
- A broken seam is caught by the check, before you see it on the dashboard.
- When the agent says it is done, a test scenario proves it.

## Signs that it slips

- The agent builds before the questions are answered. Ask it: "Is the interview done?"
- A file and the code disagree, and nobody noticed. Add a check.
- Your answers stay in the chat. Move them into the files.
- The plan grows past what you meant. Ask what each item is for (chapter 9).

## Exercise

Pick your project and fill in this sentence before you start: "Part one is ..., part two is ..., and the thing they share is ...". If you cannot name the shared thing, pick another project.
