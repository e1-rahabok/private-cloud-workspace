# 1. Why small chats fail

## The pattern

Most people start with an AI coding agent the same way: one small request per conversation. "Add a column." "Fix this error." "Rename that." Each request works. After a few months there are thousands of conversations and a system that nobody, human or AI, fully understands.

The author of this workspace built four connected repositories this way. The result worked, but it cost too much time, and every new request started with the agent learning the system again.

## What goes wrong

**Each conversation starts empty.** The agent does not remember yesterday. Whatever it learned about the system is gone unless it was written into a file it reads.

**Gaps get filled silently.** When an instruction does not decide something, the agent picks a plausible answer and moves on. In a small task that is harmless. In a long task, the next twenty steps are built on that guess.

**"Done" means "looks done".** Without a check, the agent's report that a task is finished is its own opinion. It reports a mistake in the same confident tone as a success.

**Facts get copied.** The same definition ends up in several places: a threshold in the knowledge base, in the code that computes it, and in the screen that shows it. Each copy is changed by a different conversation. They drift apart.

**The seams are invisible.** Inside one repository, tests and rules protect the code. Between repositories, nothing does. In this workspace, a change to a response field in one repository would have made the other show "service unavailable", and no test in either repository would have failed. Chapter 6 shows the check that now catches it.

## What does not fix it

- **A longer prompt.** It is read once and forgotten next session.
- **A bigger model alone.** A stronger model fills gaps more cleverly, but it still fills them.
- **More small chats.** Each one adds a little drift.

## What does

Write down, in files the agent reads every session, the few things that keep it on track, and check the meeting points with code. That is the method in [chapter 2](02-the-method.md).

## Exercise

Pick a project you have built with an AI agent. Write down three facts about it that exist in more than one place. For each, which copy is the real one? If you cannot answer, that is your first seam.
