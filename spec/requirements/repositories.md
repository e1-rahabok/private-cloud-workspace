# Requirements: repository clean-up

The clean-up in milestone M2 that is not a contract: knowledge that sits in the wrong repository, an outdated plan, old benchmarks, and old names. IDs are explained in the [glossary](../glossary.md); question IDs point at the interview ([round 1](../interview-round-1.md), [round 2](../interview-round-2.md), [round 3](../interview-round-3.md)).

## Knowledge in the right place

### R-REPO-001 Every fact in PCM-Adapter's knowledge pages exists in Agent E2 first

Milestone: M2.

Source: W-025 (the adapter's documentation points to the knowledge instead of repeating it); W-001 (Agent E2 owns domain knowledge).

Given PCM-Adapter's knowledge pages: [docs/concepts/capacity-management.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/concepts/capacity-management.md), [docs/concepts/kpi-scoring-models.md](https://github.com/e1-rahabok/PCM-Adapter/blob/main/docs/concepts/kpi-scoring-models.md), and the explanatory sections of the pages in [docs/reference/metrics](https://github.com/e1-rahabok/PCM-Adapter/tree/main/docs/reference/metrics)
When their facts are compared with Agent E2's knowledge base
Then every fact is found in a knowledge file, or is added to one through a source note before anything is removed from the adapter
And a fact that contradicts the knowledge base is listed for the author to settle, never silently dropped

Test scenarios:
- T-REPO-001a (anywhere, manual with an AI comparison): extract the claims of each adapter page; for each, name the knowledge file and line that holds it, or the source note that adds it. Expect a complete table with no claim unaccounted for, kept in the pull request that removes the pages.

### R-REPO-002 PCM-Adapter's documentation keeps only what the adapter does

Milestone: M2.

Source: W-025; the author's message of 2026-11-26 naming the adapter's concept and metric pages as knowledge that belongs to Agent E2.

Given PCM-Adapter's documentation after R-REPO-001
When a reader opens a metric or concept page
Then it describes what the adapter computes and publishes (keys, inputs, settings, states) and how to install and run it
And for what a metric means and how to use it, it links to the Agent E2 knowledge file (until isvara.io's articles exist in M5, then to the article)
And the README presents the adapter as one part of Private Cloud Manager, with links to Agent E2 and PCM, and names the simplest deployment: the pak file alone

Test scenarios:
- T-REPO-002a (anywhere, manual review by a fresh session): read every page of the adapter's docs; expect no explanation of a metric's meaning beyond one sentence, and a knowledge link on each metric page.
- T-REPO-002b (anywhere, automated by the adapter's existing link check, [check_links.py](https://github.com/e1-rahabok/PCM-Adapter/blob/main/tools/check-docs/check_links.py)): expect no broken link after the pages are removed.

## Agent E2's repository for release 1.0

### R-REPO-003 Agent E2's plan describes release 1.0

Milestone: M2.

Source: Q-6 (round 1: "Update Agent E2's plan. It's outdated."); Q-58 (round 2: milestones A1 to A6).

Given Agent E2's [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md)
When a session reads it at the start of work
Then its milestones are A1 to A6 as decided in Q-58, with the items of the on-premises deployment (local model, offline bundle, live test with blocked network) listed as parked
And its fine-tuning row points to the workspace's [design note](../design/fine-tuning.md)
And agent-e2's CLAUDE.md sends questions that bind several repositories to this workspace (W-019)

Test scenarios:
- T-REPO-003a (anywhere, manual review): the plan's milestone table has A1 to A6 and a parked row for the on-premises deployment; agent-e2's rules check passes.

### R-REPO-004 The older benchmarks are removed

Milestone: M2.

Source: Q-12 (round 1: "Remove them permanently."); Q-59 (round 2: what is removed and what stays).

Given the older benchmark material listed in Q-59
When the removal is merged
Then the result folders from before 2026-11-16, the retired questions, the old harness code and its design notes, the old plan decisions and review, and the retrieval results of 2026-11-14 are deleted from main
And the round of 2026-11-16 and the question-set history files stay
And the free-text judge's scoring rubric is kept first, in agent-e2's benchmark folder, for the new grader of M10
And the live documents that quote old numbers (MISSION.md, README.md, harness/README.md, harness/AGENT.md, benchmark/design.md, benchmark/models.md) are rewritten without them
And git history is not rewritten

Test scenarios:
- T-REPO-004a (anywhere, automated by agent-e2's rules check and its unit tests): both pass after the removal.
- T-REPO-004b (anywhere, automated by a link search to write): no file on main links to a deleted path.

## Names

### R-REPO-005 The product is called Private Cloud Manager

Milestone: M2.

Source: Q-60 (round 3: "Manager, not Management"); W-028.

Given PCM's documents and its decision log
When a reader meets the product's full name
Then it is "Private Cloud Manager", in PCM's README, its design documents and D-001
And "Private Cloud Management" remains only where it names the discipline or the author's books

Test scenarios:
- T-REPO-005a (anywhere, manual review): search PCM's documents for "Private Cloud Management"; expect each remaining use to name the discipline or a book.

### R-REPO-006 No repository uses an old repository name

Milestone: M2.

Source: Q-3 (round 1: rename references, archives left as they are); W-007; W-028.

Given the repositories agent-e2, PCM-Adapter, private-cloud-manager, isvara and this workspace
When their files outside archives and dated records are searched
Then none contains "VCF-vCommunity-Adapter" or "private-cloud-management"

Test scenarios:
- T-REPO-006a (anywhere, automated by a check to write in [checks](../../checks), run by run_all.py): search the clones for the two old names outside archives and dated records; expect no match. Today: about 10 files in agent-e2, 1 in PCM, and the adapter's own files.
