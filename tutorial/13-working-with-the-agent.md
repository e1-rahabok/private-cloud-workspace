# 13. Working with the agent

## Division of work

The person is the domain expert and the user. The agent is the architect and the implementer. Each gives what the other cannot.

- **The person gives input:** the goals, the scope and what success means; who the users are and what they expect; the domain knowledge, such as the KPIs, their limits and how operations teams work; the constraints and the reasons behind them; the assumptions only field experience can confirm; names that carry identity; and acceptance of each milestone on its review page.
- **The agent decides and writes:** the survey of the code; the requirements, drafted from the input; the design, covering security, scalability, performance, reliability and maintainability; the contracts and the master copy of each shared fact; numbers derived from the input; the checks, the code and the tests.
- **Both write together:** the acceptance criteria, the test plan, the risks, the dependencies and the glossary.

## Input and rulings

For most of this project the split was drawn differently. The person made the decisions; the agent asked for them, recorded each answer as a numbered decision, and carried it out. The author named the flaw on 2026-11-28: "You record all decisions in DECISIONS.md. This makes you take my decisions as the authority, and then jump into execution. Decision is yours, not mine." And on what the agent should bring instead: "You come to me not for decision, but for scope, goals, requirements, assumptions, constraints, and rationale."

The decision log had made the habit worse. Once an answer was a numbered decision, it read as an order, and an order gets executed. The clearest case is in the log itself: WD-022 recorded the author's table of reasons why visitors come to isvara.io as a decision, and the site plan was rebuilt around it within the hour. Its status line was later changed to read: "The visitor model was a suggestion". The next section tells the story.

Three habits follow from the new split:

- **Ask for knowledge, and decide the rest.** A question to the person asks for a goal, a fact, a constraint or a reason, and says what the agent will assume until the answer comes ([chapter 5](05-the-interview.md)).
- **Show the design.** The person reads the design to learn and to catch a domain mistake, so each choice carries its options and its reasons ([chapter 8](08-design.md)).
- **Write the outcome where it takes effect.** An answer changes the brief, a requirement or the design directly, with the person's words as the reason ([chapter 2](02-the-method.md)).

Since 2026-11-28 the [CLAUDE.md](../CLAUDE.md) of every repository in this project states these roles in a section of their own. One line in it carries the change: "Ask the author only for input. Never ask the author to approve a design choice or to choose between designs."

## The agent as co-architect

The division above says what the agent does. This section is about how it should think while doing it.

An agent is very good at carrying out instructions, and that is exactly the risk. In this project the author shared a table of reasons why visitors come to the public website: to read, ask, listen, solve, catch up, and so on. It was meant as input for a design discussion. Within the hour the agent had recorded it as a formal decision, rebuilt the whole site plan around it, added six features and merged the change. The author's reply was short: you are behaving like a doer; I need a thinker; that was a suggestion, not an instruction.

- When the agent then did think about it, it found real weaknesses. The table mixed what visitors want done with the format they prefer. It multiplied the number of AI-written forms of content that nobody had time to review. And it left out what made the site unusual. The author then proposed a better backbone of three learning paths, and that discussion produced most of the final design. None of this happens if the agent executes first.

What a co-architect does differently:

- **Treats the person's input as material to think with.** Unless the person says "decide" or "do it", a suggestion gets a reply first: what is strong in it, what is weak, what is missing, and a recommendation. The files change only after the two agree.
- **Disagrees when it has a reason.** A recommendation that simply repeats what the person said is not worth asking for.
- **Decides what it can decide.** The agent in this project asked where "availability" belongs among operations disciplines. Any practitioner knows the answer. Asking wastes the person's time and costs their trust. Questions are for input: goals, scope, facts from the field, constraints and reasons. For everything else the agent states its answer with its reason, and the person can correct it.
- **Checks the plan against the person's intent.** At the start of a release, the agent compares what the person says the release is with what the roadmap holds, and shows the difference with numbers. In this project the person expected two parts to stay nearly untouched; the roadmap held 43 requirements for them.
- **Leaves names to the person.** A name tells people who a project belongs to. The author once let the agent rename the management pack, then reversed it to keep the community's name. Naming is taste, even when it is delegated.
- **Looks before it asks.** Before any question, the agent searches the brief, the design, the requirements, the interview records and the glossary. In this project it once asked whether the management pack was "part of" PCM. Three files already held the answer, and the question used a word with two meanings. It now describes such relations by mechanism: which code, which network call, which data, which dependency.
- **Says what it does not know.** When asked whether technical podcasts are popular, the useful answer separates what it knows, what it believes, and what it has not checked.
- **Treats the person's money as input.** The person pays for every model call a test makes. A test that spends is first shown with its price, its time and what it proves, and starts only on the person's go; a budget caps a run and approves none.

Write these expectations into the agent's working rules ([CLAUDE.md](../CLAUDE.md)). An agent forgets them under pressure to make progress, as this one did more than once.

## Asking good questions

- When the agent does ask, each question should stand on its own: the files involved, what they say, what is blocked, the input needed, and what the agent will assume until the answer comes. The person can then answer in a word, or not at all if the assumption holds. [Chapter 5](05-the-interview.md) covers this in detail.

## Correcting the agent

Corrections are the most valuable thing the person gives. Put each one into a file so the next session starts from it. In this project the author corrected facts ("the demo data stays") and also the agent's framing: it had treated a benchmark as a contest to win, when the author only cared that the product works. Both kinds of correction were written down.

### The architect, then the implementer

A wrong fact in a file usually means the specification does not hold the right one. The agent has two roles, and a correction passes through both, in order. The author drew the flow on 2026-11-28:

> Me --> Give corrections, addition, changes.
>
> You (The Architect) --> update the docs. Requirements, milestone,
>
> You (The Implementer) --> build, execute, code the actual changes.

- **As architect,** the agent finds why the specification missed the fact, and changes the specification: the brief, a requirement, the design, the test plan or the roadmap.
- **As implementer,** it changes code and documents only from the changed specification. It searches the files for the fact the specification now states, in any wording. A search for the person's own words finds the sentence they pointed to and misses the others.
- **In its report,** it speaks as the architect: what went wrong and why, what the specification now says, then what was built from it. The implementer never addresses the person.

The rule came from a correction the agent handled as a prompt. The author pointed to a sentence in isvara's README that said the books are published on a Box share, and the agent changed that sentence. The author found a second one in the same file and asked: "I thought you've cleaned them up?" The agent then searched for Box and changed what it found, and the author replied: "You again jump into "iterative prompting" mode. Stay in SDD mode. You should think WHY you missed them." The cause was a gap in the specification. No item said where the books come from, and the READMEs and CLAUDE-PROJECT.md files had been written before the specification and never read against it. As architect, the agent added DEPENDENCY-10 to the brief: the master copies are on the author's laptop, and the author uploads each edition to Vercel Blob. It added R-WS-009, under which a fresh reviewer reads every README and CLAUDE-PROJECT.md against the specification. As implementer, it then searched isvara's files for that fact, and found three statements the search for Box had missed: two called the Blob copy "the source of truth", and one said to download a new edition "when it is published". The [CLAUDE.md](../CLAUDE.md) of every repository now names the two roles in its section Roles. [Chapter 16](16-case-study.md), day six, has the whole case.

The person is the expert in the field, and may not be a software developer. Write each reply for the person's background, which the brief's section on users states. Name each thing by what it does. An ID, an abbreviation, a tool name or a file path means something to the agent and nothing to the person; link a file only when the person must open it. The author of this project put it plainly: "Jargons like LPG and CI are aliens to me as I'm not a software developer. I'm just a vibe coder."

## Choosing a model and effort

Use the strongest model and a high reasoning effort where a mistake spreads: surveying the system, writing the map and the requirements, and reviewing finished work against the requirements. A cheaper, faster model is fine for work that is already fully specified.

A stronger model is not a cure for the problems in this chapter. The skipped interview and the decision taken from a suggestion both happened on the strongest model available, at high effort. The rules in the files and the person's questions prevented them from happening again; a bigger model would not have.

Effort is a setting someone has to be able to see. When the author asked for a high effort on 2026-11-28, the project's main chat ran at a fixed low effort, so the deep work moved to separate threads, where the effort can be raised. Put work that needs depth where its setting is visible.

To compare models, give two of them the same slice and the same files, and count how much rework each needs, using your checks and a review in a fresh session.

## Documents for people and machines

Some documents are mainly for people: the readme, the brief, the design, this tutorial, commit messages. Others are mainly for the agent: its working rules (CLAUDE.md), the requirements, the templates. They are written differently, and each kind has its own rules.

**For people,** the rules began as the ones the author had worked out in the knowledge service's repository ([writing.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/writing.md)), after fixing AI-written text there several times. In milestone M2 of the [roadmap](../ROADMAP.md) they moved to this workspace's [writing rules](../writing/README.md), so every repository follows one copy. In short:

- plain sentences, with the fact itself rather than filler;
- none of the phrases on a list of typical AI wording, each listed with its plain replacement, kept in one file in this workspace ([flagged-phrases.yaml](../writing/flagged-phrases.yaml));
- no slogans and no "X, not Y" constructions;
- headings that name the topic, as in a reference book: "Stop conditions" rather than "When the agent must stop";
- short table cells, with bullets instead when the text is long, because GitHub squeezes wide tables.

A script ([tools/style.py](../tools/style.py)) reads that list, so the rules exist in one place, and checks every document for people in every repository on each pull request, against each repository's own baseline of known problems. It cannot spot a slogan or an "X, not Y"; those need a reader, who should judge each line together with the lines around it.

**For the agent,** the aim is to be followed exactly: one rule per bullet, the trigger before the action ("Before each commit, run…"), exact file paths and names, and no history or attribution the agent has to skip.

Two rules apply to both kinds, and a second script enforces them ([tools/docs.py](../tools/docs.py)):

- Every file reference is a clickable link: relative inside the repository, a full GitHub address for another repository. A reviewer clicks instead of searching.
- Every diagram is an SVG drawn by a script ([tools/diagrams.py](../tools/diagrams.py)), with its text generated from the SVG and placed underneath in a folded block. People see the picture and a model reads the text. The check fails if the two no longer match. There are no drawings made of text characters, which break on narrow screens and are hard for a model to read.

The agent had read those repositories and still ignored both conventions at first. A convention the agent knows about is not one it follows. Only the script made them stick.

## A fresh reviewer

Review finished work in a new session that sees only the requirements and the change. It has not followed the implementer's reasoning, so it notices different mistakes. The rule holds for documents too. R-WS-009 asks a fresh reviewer to read every README and CLAUDE-PROJECT.md against the specification. The session that first read them found and fixed seven disagreements, and still left the review open: having read and edited the files, it was no fresh reader of them.

## Secrets

The agent never sees a password. Here, credentials are encrypted files that only the author's Windows account can decrypt, created by the author with a command that prompts for the password. Scripts load them, and nothing prints, logs or commits them. On the lab's Linux virtual machine they sit in an environment file that only root and the `pcm` group can read (DESIGN-9 in the [system design](../spec/design/system.md)).
