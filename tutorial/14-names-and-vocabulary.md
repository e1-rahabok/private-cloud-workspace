# 14. Names and vocabulary

## Names and the agent

Every session reads your files with no memory of the last one. A name that needs explaining costs every reader, every time, and an agent that guesses a name wrong builds on the wrong guess. The author's rule for this project: "The best documentation is No Documentation." A name that explains itself needs no page about it.

A VMware administrator already knows this from naming conventions. A VM called `sg1-prd-sql-03` tells you the site, the environment, the role and the instance at 2 a.m., without a spreadsheet. Files, folders, IDs and terms in a project deserve the same care, because the agent reads them all day.

## One word per concept

In this project "stage 1" and "release 1.0" named the same scope, and "stage" also named a step inside Agent E2's answer pipeline. Three meanings shared two words. The fix:

- **Release 1.0** is the goal; **milestones** M1, M2 and onward are its steps.
- The other meaning of "stage", inside Agent E2, keeps its word, because it is a different concept.
- The [glossary](../spec/glossary.md) maps the old words to the new ones, so old notes can still be read.

Before adding a new term, check that it overlaps with no existing one. Two words for one thing, or one word for two things, both make the agent guess.

## IDs a reader can guess

Workspace decisions were numbered W-001 to W-029. Nobody could guess what "W" stood for, and it sat next to PCM's own D- decisions. They became WD-, for "workspace decision": 208 references in 26 files, renamed in one change. Other IDs in this project follow the same pattern:

| Prefix | Means | Example |
|---|---|---|
| GOAL- | An outcome the product must bring about, in the brief | GOAL-3 Value without the author |
| CONSTRAINT- | A limit the design must accept, in the brief | CONSTRAINT-6 The lab is reached only from the author's laptop |
| RISK- | What could go wrong, and who acts on it | RISK-2 No licence gives no right to copy |
| DESIGN- | A design choice, with its reason and rejected options | DESIGN-17 Missing data never shown as a value |
| Q-WS-, Q-E2- | A question for the author, with the repository it belongs to | Q-WS-120 Where the nested ESXi hosts run |
| R-ADP- | A requirement on the VCF vCommunity Adapter | R-ADP-018 No value from a partial read |
| T-ADP- | A test scenario of that requirement | T-ADP-018a |

The brief also uses SCOPE-, PRINCIPLE-, ASSUMPTION- and DEPENDENCY-, each named for the kind of statement it holds ([chapter 6](06-constraints-assumptions-risks-dependencies.md)). The WD- prefix is retiring with the decision log: its outcomes now live in these IDs, and the [glossary](../spec/glossary.md) keeps WD- so old notes can still be read.

## Numbers in the order of work

Milestones added later got the next free numbers, M8 to M10, but had to be built before M3. The roadmap then read M2, M8, M9, M10, M3, and every reader had to work out the real order. They were renumbered so the numbers give the sequence.

Numbers change again when scope changes. When a milestone was removed from release 1.0 later, the numbers jumped from M3 to M5. The renumbering waited until the scope had settled, so it was done once.

A milestone inserted before the first one got the numbers M0 and then M-1. The author's reply: "A project first milestone is called Milestone 1." Work that prepares the agent is done before the milestones and is not one of them; the milestones start at M1, and the milestone gate fails when the numbers do not run M1, M2, M3 in order. M-1 also clashed with PCM's demo story M-1.

## Folder and file names

- **No version, milestone or status words.** `pcm_proto`, `v5`, `new`, `old` and `final` all stop being true. Git keeps the history.
- **No bare IDs in a name.** `l2_story_m5.py` names its demo story by its ID, M-5. A reader took the ID for milestone 5.
- **Group by what one task needs.** PCM's files were grouped by phase: specifications, design, code, deployment. One workspace of the app was spread over six folders, so every session had to collect it. They are now grouped by workspace, and one folder holds the whole context of a task.
- **Use full words.** `executive` reads better than `exec`, and `agent-e2` better than `e2`.

## Renaming everywhere

- When a name or number stops being true, rename it in every file. Never add a note that explains the exception, because each note is one more thing every session must read and remember. Renaming across many files is safe only with checks: here, scripts fail on a broken link or a requirement that cites an ID that does not exist ([chapter 11](11-checks.md)).

A planned check goes further: a fresh session sees only the folder tree and guesses what each folder holds. Every wrong guess is a name to fix.

## Names that belong to people

Some names carry identity, and only the person can choose them:

- The product is **Private Cloud Manager**. The author's books keep **Private Cloud Management**, the name of the discipline: the concepts, the framework and the practice. The software implements what the book teaches.
- The management pack keeps the name **VCF vCommunity Adapter** and the metric prefix `vCommunity|`. The agent had chosen "PCM" for both when the author delegated the naming. The author reversed it: the pack is a vCommunity project of vExperts and VMUG members, and the name shows a grassroots effort.

The agent can propose names that are short, guessable and free of overlap. Whether a name says the right thing about who made it, and for whom, is the person's call.

## Exercise

Show your agent only the folder tree of one of your repositories, with no file contents. Ask it what each folder holds. Count the wrong guesses, and rename until it guesses them all.
