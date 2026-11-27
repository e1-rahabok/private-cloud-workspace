# isvara.io before and after

The change to isvara.io in release 1.0, feature by feature: what the site does today, what it will do, and who decided it. The author asked for this document to review before anything is built (answer to Q-WS-41, [interview round 1](../interview-round-1.md)). The requirements of milestones M4 to M7 in [ROADMAP.md](../../ROADMAP.md) are written from it, and M4 starts only after the author's review. The plan it details is [isvara-plan.md](isvara-plan.md); IDs are explained in the [glossary](../glossary.md).

## Basis of each decision

Each item names its basis:

- **Author:** the author's own answer or decision, with its ID.
- **Round 2:** decided by Claude at the author's request on 2026-11-26 ([interview round 2](../interview-round-2.md)), with its ID.
- **Claude's call:** decided in this document, with its reason, under the author's delegation of the plan's details ([isvara-plan.md](isvara-plan.md)). These are the items to review first.

To review: write "Approved" under the heading Review at the end, or name a feature and the change.

## The site in one view

- **Before:** a reading site over the author's five books (the Executive Summary and Parts 1 to 4), converted from Word into HTML chapters. AskIO answers from the whole book in its context. Ten tools, an RVTools health check, the 2am game and downloads sit around it.
- **After:** a site over Agent E2's knowledge base. Each knowledge file becomes an article, reached through the three learning paths and their crossings. Agent E2 answers questions. Visitors contribute corrections and files, practise with a quiz and an exam, and see what changed each week. The books stay downloadable.
- **Kept:** the Signal design, its look and its two themes (Author, Q-WS-44); the 2am game, the RVTools health check, downloads, the MCP endpoint, Team and Homelabs.
- **Gone:** the book reader, AskIO, the Operations Score, the self-assessment, the cost calculator and the SLA builder (Author, WD-027).

## Knowledge presented for the web

The author called this the hard part: the book as HTML pages wastes the web, and the site should offer several ways to slice the knowledge (answer to Q-WS-43). The design uses what each knowledge file already carries, so isvara.io adds no structure of its own (Author, WD-001, WD-027).

### Contents of a knowledge file

- A title, sections, and a Misconceptions section in almost every file.
- Metadata: its form (`retriever_guide`: how-it-works, metric-meaning, what-to-set, health-check, troubleshooting, decision-tree), its tags for the three paths (`technology`, `pillar`, `product`, `object`), and for metrics the `layer` and `metric_class`.
- Links: `related` (read together) and `internal_derive` (the files it builds on).
- Images with their own tags, and in some files a Mermaid diagram.
- `source.path`: the book heading the file came from, where it came from a book.
- Catalog rows: the limits, bands and models in [Agent E2's catalog](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge/catalog).

### Articles

- **Before:** a chapter page is a slice of a book, up to about 25,000 words, at `/read/<book>/<page>`.
- **After:** one article per knowledge file, at `/articles/<id>`, for example `/articles/vsphere/technology/cpu/metrics/virtual-motherboard/ready` (Round 2, Q-WS-101 for the source view).
- **The text:** an AI rewrite into plain prose that keeps every fact, number and section of the file, adds none, and follows the writing rules (Author, Q-WS-42; WD-023).
- **Common misreadings:** the file's Misconceptions as a box at the end, each with its correction (Author, WD-017).
- **Numbers:** every limit and band is drawn from the catalog row, never typed by hand (R-CONTENT-001). A metric's five limits show as a coloured band bar; a reader moves a slider to see a value's band. Claude's call: the catalog makes numbers interactive at no cost in accuracy.
- **Diagrams:** a Mermaid diagram in the file is drawn as an SVG, with its text underneath. Claude's call: the same rule the workspace follows (WD-020).
- **Flows:** a troubleshooting, decision-tree or health-check file shows its checks as steps a reader opens one by one, with the branch to the next file. Claude's call: a flow is a sequence, and a reader at 2 a.m. wants the next step.
- **Where the reader is:** a trail at the top (path, topic, article), chips for the article's other paths, "Read first" from `internal_derive`, "Read with" from `related`, and the neighbours in the same topic (Author, WD-027 through the plan).
- **Source:** a link to `/articles/<id>/source`, the file as the model reads it, with the note that it is written for an AI model (Author, Q-WS-45; Round 2, Q-WS-101).
- **Footer:** "Written by AI from Agent E2's knowledge base, which is still being reviewed." (Round 2, Q-WS-103).
- **Dates:** "last changed", and "corrected on" when the weekly summary marked a change as a correction (Author, WD-027 through the plan).
- **Ask about this article:** opens Ask with the article named, so Agent E2 reads it first (Round 2, Q-WS-97; R-E2-022).

### Four lenses on every topic

A knowledge file's form says which lens it serves. The lenses are a completeness check, and the quiz uses them to tell a reader what they are missing ([knowledge model](../knowledge-model.md)).

| Lens | Forms |
|---|---|
| How it works | how-it-works |
| How it is measured | metric-meaning; the catalog |
| How it is managed | what-to-set, health-check; the SP5 framework files |
| How it fails | troubleshooting, decision-tree |

- Claude's call: the mapping uses the forms as they are; no file gets a new tag.

### Three paths and their crossings

- **Before:** `/guide` shows a node map of the five books and their chapters.
- **After:** `/learn` opens the three paths (Author, WD-027):
  - Architecture: CPU, memory, storage, network, from the `technology` tag.
  - IT management: availability, performance, security, capacity and value, from the `pillar` tag.
  - Product: vSphere, vSAN, NSX, VCF Operations, Kubernetes, Windows, Linux, then by object type, from the `product` and `object` tags.
- **Topic pages:** `/learn/architecture/cpu`, `/learn/management/performance`, `/learn/product/vsphere/cluster`. Each shows its articles in four columns, one per lens, so a gap is visible.
- **Crossings:** any topic page narrows by the other two paths, and each narrowing has its own address, for example `/learn/architecture/cpu?pillar=performance&object=cluster` (Author, WD-027 through the plan).
- **Start here:** each topic page lists its articles in a reading order where every article comes after the files it builds on (`internal_derive`), and how it works comes before how it is measured, managed and how it fails. Claude's call: this answers the order question of Q-WS-43 from data the files already hold.
- **Empty lens:** a lens column with no article says so and links to Contribute. Claude's call: the knowledge model asks the coverage table to show where help is needed.
- **Tag `system`:** files tagged `system` (across CPU, memory, storage and network) show under Architecture as "Across resources". Claude's call: the tag exists in the files and the plan's list of four leaves it out.
- **Value:** the files tagged `value` show under IT management, value, and nothing new is added for it (Author, WD-034).

### Search

- **Before:** the ⌘K palette scans the books' headings and text.
- **After:** the palette searches articles, the glossary, misreadings and metric names. The words people use map to the knowledge base's terms through Agent E2's `user-terms` catalog. A switch allows regular expressions (Author, WD-027 through the plan).
- Claude's call: the index is built at build time in the browser bundle, with no search service, as today.

### Infographics

- **After:** a core feature (Author, WD-027). Each is an SVG drawn by code from a knowledge file, with its text underneath. The first is the I/O path, from application to array (the knowledge model's example of each team reading its own layer).
- Claude's call: an infographic draws only facts of the files it cites, and each cites them.

### The rewrite and its checks

- **When:** every article is rewritten once; after that, each week, only the files changed by that week's knowledge commits (Author, WD-027 through the plan).
- **Model:** Gemma 4 31B and one stronger model are tried on a pilot article; the cheaper one that passes the checks is used (Round 2, Q-WS-106).
- **Checks before publishing:** every number of the file appears, every section appears, the misreadings appear, the wording passes the style check, every link resolves, and a judge finds no claim the file does not support (Author, WD-027 through the plan).
- **Where the rewrites live:** committed to isvara with the knowledge commit they were written from, so pages are static and reviewable in a pull request. Claude's call: a page then never calls a model when a visitor reads it.
- **Where the knowledge comes from:** Agent E2's export (contract C4), read at a pinned agent-e2 commit. A weekly workflow moves the pin, rewrites the changed files and opens a pull request. Claude's call: the pin makes every build repeatable, and the pull request shows the week's changes.

## Feature by feature

### Pages that go

| Feature | Before | After | Basis |
|---|---|---|---|
| Book reader | `/read/<book>/<page>` chapters | Redirect to the article for that book heading | Round 2, Q-WS-100 |
| Guide map | `/guide`, `/guide/<book>`, `/map` | Redirect to `/learn` | Claude's call |
| Self-assessment | `/assess`, `/result` | Gone; the mastery map replaces it | Author, WD-027 |
| Operations Score | `/tools/ops-score` dial | Gone | Author, WD-027; Q-WS-49 |
| SLA builder | `/tools/sla-builder` | Gone | Author, WD-027 |
| Cost calculator | `/tools/cost-calculator` | Gone | Author, WD-027 |

- **Redirects:** each old `/read/<book>/<page>` address goes to the article whose `source.path` names that page's first heading, from a frozen copy of the old chapter index; an address with no match goes to `/learn`. A `#fragment` never reaches the server, so the browser keeps it across the redirect and a script on the article takes the reader to the article of that heading. Every redirect is permanent, so search engines move their links. Claude's call for the mechanism.

### Ask

- **Before:** AskIO at `/ask`: Gemini 2.5 Flash or Flash-Lite with the whole book in its context, cite chips to `/read`, the ops-score pill, four cached sample questions, thumbs up and down.
- **After:** Ask Agent E2 at `/ask` (Author, WD-004, WD-017):
  - a conversation over several turns, where Agent E2 may ask for another screenshot, a CSV file or a longer history;
  - up to 5 screenshots of 5 MB and 3 CSV files of 2 MB, with a box the visitor ticks to confirm IP addresses and host names are removed (Round 2, Q-WS-95; Author, WD-024);
  - the stage and the time so far while Agent E2 works, read every 10 seconds, and a message when it stops responding (Author, WD-043; R-ASK-002);
  - sources as links to articles and their source view (Author, Q-WS-45);
  - Day 0 and Day 1 questions answered with a pointer to Broadcom's documentation (Author, WD-026);
  - thumbs up and down kept, stored with the question, the answer and Agent E2's trace ID (Round 2, Q-WS-61).
- **Kept from AskIO:** select-to-ask in an article, the Ask button and ⌘I, the shared thread across pages, the names of an RVTools report swapped for stand-ins before they leave the browser.
- **The injection guard** stays in isvara.io, before Agent E2 is called (Author, Q-WS-47, WD-017): the pre-scan and the fenced user turn. Rule 4 of AskIO's prompt, the layer that stops an attack today, loses its place when Agent E2 writes the prompt; where it goes, and how the two eval batteries change, is open question Q-WS-136, before M5.
- **Where Agent E2 runs:** measured in M5 on a Vercel Python function and a small container host; a container host is preferred, since answer jobs live in memory (Author, Q-WS-4; Round 2, Q-WS-94). It answers only calls carrying isvara.io's secret (Round 2, Q-WS-98).
- **Sample questions:** four, answered by Agent E2 ahead of time and served from a cache, as today. Claude's call: a first visitor sees an answer at once, at no model cost.

### Contributions

- **Before:** none.
- **After:** `/contribute` (Author, WD-024): a correction, an addition, something to review, or a request for a session at a VMUG event; one area, a note of up to 2,000 characters, one link and up to three files (PNG, JPEG, CSV).
- **Queue:** private; nothing is published by itself. Each week AI sorts the queue and the author decides; accepted items become source notes in agent-e2, with credit when the contributor gave a public profile link (Author, WD-024).
- **Kept:** files until processed and at most 30 days; no IP address with a contribution; no email address asked (Author, WD-024).
- **Review page:** a key-gated `/admin/contributions`, like today's `/admin/questions`. Claude's call: the author already reviews questions there.

### Protection

All from the plan's Protection table (Author, WD-024; Round 2, Q-WS-61, Q-WS-104, Q-WS-105):

- Vercel's firewall rate limits, 60 requests a minute per address (Claude's call), and an "under attack" switch against floods.
- An invisible bot check and a hidden field before Ask and Contribute.
- 10 questions an hour and 30 a day per address; 3 contributions a day per address; 100 contributions a day in all.
- Files checked by content, image metadata removed, and every image checked by a model to be an IT screenshot.
- A daily stop on model spending of about US$1.65, within US$50 a month on the gateway, counted from tokens and a price table, over Ask and isvara.io's own model calls; the weekly rewrites report their cost in their pull requests (Claude's call for the counting).
- One switch each that closes Ask or Contribute without a redeploy.

### Practice

- **Before:** the 2am game, and five practice questions inside the self-assessment.
- **After:** `/practice` holds four things (Author, WD-027):
  - **Quiz:** short rounds on one path or crossing, drawn from a pool so a visitor can come back; each wrong answer links to the section that explains it.
  - **Mastery map:** the paths as a grid against the four lenses, filled in as the visitor proves each part ("strong in how CPU works, weak in how it is measured"), kept in the browser.
  - **Exam:** `/exam`, ten very hard questions, four options, +3 and −1, dated (Author, WD-006; Round 2, Q-WS-109 to Q-WS-118; requirements in isvara's [exam.md](https://github.com/e1-rahabok/isvara/blob/main/spec/requirements/exam.md)).
  - **Daily question:** one question a day for everyone, with the share of visitors who got it right.
  - **2am game:** kept; its debriefs cite articles, and its numbers are checked against the knowledge files. Its nightly board, one per UTC day, stays as it is. Claude's call: WD-027's dropped global board is the quiz's.
- **Comparing scores:** anonymous percentiles, a share card, and boards for one event with a room code; no global board (Author, WD-027).
- **Quiz questions:** written from the misconceptions of the files they cite, each with the files' fingerprints, checked by a judge, and stopped from building when a cited file changes, as the exam's are (Round 2, Q-WS-112). Claude's call: the pool holds at least 10 questions for every topic with at least 10 articles; the author approves the exam's ten and reviews 20 quiz questions, since the quiz is open-book practice.
- **Header:** the exam sits in Practice beside the 2am game. Claude's call: the new header has one entry for practice (see Header and home page).

### Tools

Each tool stays only where Agent E2 holds its knowledge (Author, WD-001; Q-WS-50 left the list to this document).

| Tool | After | Basis |
|---|---|---|
| Capacity planner | Rebuilt on the catalog and Agent E2's capacity model; first | Author, WD-027 |
| Failover capacity | Kept; its articles cited in place of chapters | Claude's call |
| Super metric builder | Kept; metric keys and presets from Agent E2's files | Claude's call |
| Dashboard blueprint | Rebuilt from Agent E2's dashboard files | Claude's call |
| Cluster KPI | Gone in release 1.0 | Claude's call |
| Maturity | Gone with the self-assessment | Claude's call |
| Advanced troubleshooting | Kept, as the author's talk; cites articles | Claude's call |
| RVTools health check | Kept; each check grounded in a catalog row or a file | Author, WD-027 |
| Fleet Console | Hidden until its checks come from the catalog | Author, WD-027; Round 2, Q-WS-107 |

- **Failover capacity:** its arithmetic is the cluster's hosts and admission control, which Agent E2's cluster files explain; it holds no threshold of its own.
- **Super metric builder:** its metric keys and presets come from the knowledge files that name VCF Operations keys and hold super-metric examples; a key no file names is typed by the reader, as today.
- **Dashboard blueprint:** its personas and dashboards come from Agent E2's `sp5-framework/outputs` files, so its content has one master.
- **Cluster KPI:** a second copy of the KPI scoring, which the VCF vCommunity Adapter implements and Agent E2 explains (WD-036). The articles show each KPI's parts and limits from the catalog. Revisit after release 1.0 with a check against the adapter's scoring.
- **Maturity:** its fifteen questions are isvara.io's own knowledge; an organisation's SP5 maturity needs files in Agent E2 first, after release 1.0.
- **Advanced troubleshooting:** a talk, like the downloads, the author's own work; it computes nothing.
- **RVTools health check:** a check with five catalog limits is scored by Agent E2's KPI scoring; a check whose article gives one limit shows red or green with no score; a check with neither shows as "to review". Each cluster shows how many checks sit in each band, and the 0 to 100 cluster score goes with the Operations Score curve and the Cluster KPI weights it was built on. Claude's call: Agent E2's weighted average needs a 0 to 100 score per check, which only the checks with five limits have. The Contention area used the Operations Score curve. After, a counter is scored only where the catalog has a row for the same metric and statistic: CPU Ready and disk latency have peak rows; memory latency and a count of dropped packets have none today, so they show unscored, as "to review". Claude's call for the Contention area, since the curve goes.

### MCP endpoint

- **Before:** `ask_isvara`, `ops_score`, `health_check`, `fleet_view`, and the books as resources.
- **After (Author, WD-027; Q-WS-52 left it to this document):**
  - `ask_isvara` calls Agent E2 through the same guard and limits as Ask;
  - `ops_score` goes with the Operations Score;
  - `health_check` stays, scored as the health check is;
  - `fleet_view` is hidden with the Fleet Console;
  - the resources are the articles and the catalog, from the export, in place of the books.
- Claude's call for `fleet_view`: it opens a page that is hidden.

### The weekly What's New page

- **Before:** nothing tells a returning visitor what changed (the failure named in [intent.md](../intent.md)).
- **After:** `/whats-new`, one entry a week: the articles added, changed and corrected, and the site's own changes. Claude drafts the week's post; the author posts it to LinkedIn, X, Reddit and VMUG channels (Author, Q-WS-16; WD-027 through the plan).
- An email newsletter comes after release 1.0 (Author, WD-027 through the plan).

### Manual

- **After:** `/manual`: how customers take the product (Agent E2, the VCF vCommunity Adapter and PCM, with the workspace), the two ways to deploy, and copying each repository privately, since a fork of a public repository is public (Author, WD-025).
- Claude's call: the manual explains and links to each repository's own install steps and copies none of them, so the steps have one master.

### Downloads

- **Kept:** the books, spreadsheets, diagrams and sample reports, with "last updated" dates, refreshed weekly from Vercel Blob (Author, Q-WS-55).
- **Changed:** the weekly workflow stops converting the books into pages (Round 2, Q-WS-108).
- **New:** when a book changes, an AI comparison with Agent E2's knowledge lists only the disagreements for the author to settle (Author, WD-027 through the plan).

### Team and Homelabs

- Kept unchanged (Author, WD-027 through the plan).

### Header and home page

- **Before:** Guide, Tools, Health check, Score, 2am, MCP and Team, then the visits counter and Download.
- **After:** Learn, Ask, Practice, Tools and What's New in the header, then search, the visits counter, the theme switch and Download. Contribute, the manual, MCP, Team and Homelabs sit in the footer and the menu. Claude's call: the header carries the plan's four return reasons (learning, an expert to ask, tools, knowing what changed) and practice.
- **Home page:** the three paths, Ask, search, this week's changes and the daily question (Author, WD-027 through the plan).

### Behind the pages

- **Telemetry:** the question log, visits, feedback, downloads and tool usage stay, best-effort as today. The question log adds the answer, the trace ID and the rating (Round 2, Q-WS-61).
- **SEO:** every article and topic page gets its own title, description and canonical address, structured data, and a place in the sitemap and `llms.txt`, under the rules isvara.io follows today. Claude's call: the same rules, applied to the new pages.
- **Switch-over:** built on a branch with a Vercel preview and switched in one release (Author, WD-017; Q-WS-55).
- **isvara's own rules:** its CLAUDE-PROJECT.md describes the "load-and-ask" design without a retrieval pipeline. That design retires, and the file is rewritten in M4's first pull request (Author, Q-WS-48).

## Order of the build

The plan's order, mapped to the milestones:

1. M4 isvara.io reading: Agent E2's export (C4), articles, paths, search, the page checks, the first infographic, redirects from old addresses.
2. M5 isvara.io Ask and contributions: Ask Agent E2 with protection, the public Agent E2's host, contributions.
3. M6 isvara.io practice and tools: quiz, mastery map, exam, daily question, 2am debriefs, the tools of the table above.
4. M7 isvara.io switched over: home page, What's New, manual, header, downloads, MCP, the switch from the preview.

## Review

Reply:
