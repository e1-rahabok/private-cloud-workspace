# isvara.io plan

The design of the rebuilt isvara.io for release 1.0. It replaces the earlier draft, which listed 47 features under ten visitor reasons ([DECISIONS](../../DECISIONS.md), WD-022, now replaced by WD-027). The author delegated the remaining choices to Claude on 2026-11-26; they are recorded here as decisions. To change one, write under it or open a question. IDs are explained in the [glossary](../glossary.md).

## Purpose

- The public place where VMware administrators and architects learn to master the operation of a private cloud, ask an expert, practise, and contribute. It is never installed or copied by customers.
- The goal: recognised worldwide as the authority on large-scale private cloud performance and capacity management, based on VCF ([intent](../intent.md)).
- The problem to solve: nothing brings people back today, and they cannot tell what has changed.
- The look and feel stay; the functionality is new; the old site goes (Q-44).

## Return reasons

The author's answer to what would bring an administrator back weekly (2026-11-26): tools, an expert to ask, and learning. News is not a reason. Every part of the site serves one of these, or helps people find out that something new is there.

| Reason | Served by |
|---|---|
| Learning | The three learning paths, articles, infographics, the quiz and its mastery map |
| An expert to ask | Agent E2, with screenshots and CSV files |
| Tools | Calculators and checks built on Agent E2's catalog |
| Knowing what changed | A weekly summary, posted where the audience already is |

## Content and its source

- Every page about the knowledge is an AI rewrite of an Agent E2 knowledge file, so isvara.io holds no knowledge of its own (Q-18, Q-42). Every knowledge file is used, drafts included (Q-10).
- The rewrite keeps every fact and number of the file, adds none, keeps its sections, turns its misconceptions into a "Common misreadings" box, and follows the writing rules (WD-023). Each page passes checks before it is published: numbers, sections, misreadings, wording, links, and a judge looking for claims the file does not support.
- A page shows its source: a link to the knowledge file, with the note that it is written for an AI model to read (Q-45).
- Pages are rebuilt weekly from the knowledge commits of that week, and only the changed files are rewritten.
- The books, spreadsheets and diagrams are the author's own living work. They stay downloadable, with their "last updated" date, refreshed weekly (Q-55). When they change, an AI comparison with Agent E2's knowledge lists only the disagreements for the author to settle.

## Structure

- **Three learning paths** as the navigation: Architecture (CPU, memory, storage, network), IT management (availability, performance, capacity, configuration, security), and Product (vSphere, vSAN, NSX, VCF Operations, Kubernetes, Windows, Linux, each by object type). They come from the knowledge files' tags ([knowledge model](../knowledge-model.md)).
- **Crossings:** a reader narrows by any path and then by the others, for example CPU, then performance, then the cluster. Every narrowing has its own address and can be bookmarked.
- **Where the reader is:** a trail at the top of each article, chips for its other paths, the neighbouring articles in its topic, and "read with" links at the end.
- **Scale:** the reader says once whether their estate is small or large; "At large scale" notes are shown first for large estates.
- **Search:** one box over articles, the glossary, misreadings and metric names, with the words people use mapped to the knowledge base's terms. An advanced switch allows regular expressions.

## Features

| Feature | Decision | Note |
|---|---|---|
| Home page | Rebuild | The three paths, Ask, search, this week's changes, the daily question |
| Articles | New | One per knowledge file, with source link and reading time |
| Infographics | New, core | Generated SVG with text underneath; first: the I/O path |
| Ask Agent E2 | Rebuild | Replaces AskIO; conversations, screenshots, CSV files, sources |
| Contribute | New | A correction, a link, a screenshot or a file, for review |
| Quiz and mastery map | New | Rounds by path; shows strong and weak lenses |
| Exam | New | Ten very hard questions; marks lost for a wrong answer |
| 2am game | Keep | Debriefs cite articles; numbers checked against the knowledge |
| Calculators | Rebuild | Numbers from Agent E2's catalog; capacity planner first |
| RVTools health check | Keep | Each check grounded in a catalog row or a file |
| Fleet Console | Hidden | Back once its checks come from the catalog |
| What's New | New | A weekly summary; also posted to the audience's channels |
| Manual | New | Copying the product privately; the two ways to deploy |
| Downloads | Keep | Books, spreadsheets, diagrams; weekly refresh |
| MCP endpoint | Keep | Its ask tool calls Agent E2 |
| Old `/read` links | Redirect | To the article that covers the same section |
| Operations Score | Drop | Replaced by the KPIs PCM-Adapter publishes |
| Self-assessment | Drop | The quiz's mastery map replaces it |
| Cost calculator, SLA builder | Drop | No source in Agent E2's knowledge |
| Podcast | Drop | Agreed with the author, 2026-11-26 |
| Team, homelabs | Keep | Unchanged |

## Ask Agent E2

- A conversation over several turns. Agent E2 may ask for more: another screenshot, a CSV file, a longer history, the way the author probes wider and deeper.
- Screenshots and CSV files can be attached (Q-I1). The visitor removes IP addresses and host names first and confirms it in a box; a CSV file that seems to hold an IP address gets a reminder. No masking in 1.0 (WD-024). isvara.io keeps no copy of an attachment.
- Each answer lists its sources as links to the articles and the sections it used.
- While Agent E2 works, the visitor sees its stage ("reading the knowledge base", "checking the answer") and the time so far, and a message if it stops responding (Q-57).
- A question about design, installation or upgrades gets a short reply that Agent E2 covers operations, with a pointer to Broadcom's documentation (WD-026).

## Contributions

From release 1.0 (WD-024):

- **What can be sent:** a correction, an addition, something to review, or a request for a birds-of-a-feather session at a VMUG event, in one area, with a note, one link and up to three files.
- **Where it goes:** a private queue. Nothing is published automatically. Each week AI sorts the queue and the author decides; an accepted item becomes a source note in agent-e2, with credit if the contributor gave a public profile link.
- **Agreement:** "By submitting, you confirm that you may share this, that it holds no confidential customer data, and that it may be used, changed and published in Agent E2 and isvara.io, with credit if you give a profile link."
- **Kept:** files until processed, and at most 30 days; no IP address with a contribution.

## Practice

- **Quiz:** short rounds of multiple-choice questions on one path or crossing, from a pool, so a visitor can come back. Each wrong answer links to the section that explains it.
- **Mastery map:** the paths as a grid, filled in as the visitor proves each part, showing which lens is weak ("strong in how CPU works, weak in how it is measured"). Kept in the visitor's browser; no account.
- **Comparing scores:** as anonymous percentiles ("you beat 78% of visitors on this round"), a share card for LinkedIn, and boards for one event with a room code, such as a VMUG session. There is no global board, because an open-book quiz proves little at the top and an anonymous board attracts abuse.
- **Exam:** ten short, very hard questions; a wrong answer loses marks and a blank scores 0 (WD-006). Requirements: [isvara-exam.md](../requirements/isvara-exam.md).
- **Daily question:** one question a day, with how many visitors got it right.

## Knowing what changed

- A weekly summary of what changed in the knowledge and on the site, including corrections, marked as such.
- Claude drafts the week's post; the author posts it to LinkedIn, X, Reddit and VMUG channels (Q-16).
- Each article shows "last changed" and, when there is one, "corrected on".
- An email newsletter waits until after 1.0: it needs a provider and the visitor's consent.

## Protection

| Threat | Protection |
|---|---|
| A flood of requests | Vercel's platform protection and firewall rate limits; an "under attack" switch |
| Bots | An invisible bot check before Ask and Contribute; a hidden field bots fill in |
| One visitor submitting endlessly | 3 contributions a day per address; limits on Ask per hour and day |
| A huge file | Signed upload to storage with a size limit (WD-024) |
| A disguised file | PNG, JPEG and CSV only, checked by content; image metadata removed |
| Pornographic or violent images | A model call checks each image is an IT screenshot; others are deleted unseen |
| Instructions hidden in text | The injection guard before Agent E2; contributions are reviewed as data |
| Cost | A daily ceiling on model calls within US$50 a month; 100 contributions a day in total |
| Anything unforeseen | One switch closes Ask or Contribute without a redeploy |

The exact Vercel features and limits are checked against the current plan before building.

## Budget and hosting

- isvara.io must stay within US$50 a month on Vercel AI Gateway after go-live (WD-014).
- Where the public Agent E2 runs is chosen after measuring start-up time and cost per answer on the two options: a Vercel Python function or a small container host (Q-4). A container host is preferred, because Agent E2 keeps answer jobs in memory.

## Measures

- **Search visibility,** from Google Search Console: position and impressions for about 20 searches that define the field, monthly.
- **Returning visitors and questions asked,** from the site's counters and question log, monthly.
- **Contributions** received and accepted.

## Order of work

1. Agent E2's export for pages, its Ask additions, and the knowledge-model tags ([knowledge model](../knowledge-model.md), proposals).
2. Articles and the three paths, with search; the page checks.
3. Ask Agent E2 with protection; contributions.
4. Practice: quiz, mastery map, exam, daily question.
5. Infographics, beginning with the I/O path.
6. Calculators rebuilt on the catalog; What's New; the manual.
7. Switch over in one release from a Vercel preview, with old links redirected.
