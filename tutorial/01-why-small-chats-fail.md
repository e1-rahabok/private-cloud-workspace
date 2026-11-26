# 1. Why small chats fail

## A familiar pattern

Most people begin with an AI coding agent the same way: one small request per conversation. Add a column. Fix this error. Rename that file. Each request works, and after a few months there are thousands of conversations behind a system that nobody fully understands any more, the agent included.

The author of this project built four connected repositories that way. It worked, but it took far too long, and every new request began with the agent reading the code again to work out what the system was.

## What goes wrong

Five problems showed up, and they are common to any growing system built this way.

**Each conversation starts empty.** The agent does not remember yesterday. Anything it learned about the system is gone unless someone wrote it into a file the agent reads.

**Gaps are filled silently.** When an instruction leaves something open, the agent picks a plausible answer and carries on. In a small task that rarely matters. In a long task, the next twenty steps are built on top of that guess, and nobody knows it was a guess.

**The agent judges its own work.** Without a test, "done" is the agent's opinion. It reports a mistake in the same confident tone as a success.

**Facts get copied.** The same definition ends up in several places. In this project one performance threshold lived in the knowledge base, in the code that computes it, and in the screen that shows it. Different conversations changed different copies, and they drifted apart.

**Nobody tests where the parts meet.** Each repository had its own tests. The places where one repository relies on another had none. In one case a field renamed in one repository would have made another show "service unavailable", and every test in both repositories would still have passed. [Chapter 7](07-checks.md) shows the check that now catches it.

## What helps less than you would expect

A longer prompt is read once and forgotten in the next session. A stronger model fills gaps more cleverly, but it still fills them. More small chats each add a little more drift.

## What helps

Writing down the few things that keep the agent on track, in files it reads at the start of every session, and checking the meeting points between parts with scripts. The rest of the tutorial explains how.

## Exercise

Take a project you have built with an AI agent. Write down three facts that exist in more than one place in it. For each one, which copy is the real one? If you cannot say, you have found your first problem.
