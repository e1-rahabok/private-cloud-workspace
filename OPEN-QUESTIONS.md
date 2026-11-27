# Open questions

Questions only the author can answer. Everything else from the interview is decided; the records are [round 1](spec/interview-round-1.md), [round 2](spec/interview-round-2.md) and [round 3](spec/interview-round-3.md). IDs are explained in the [glossary](spec/glossary.md).

## Q-120 Where the nested ESXi hosts run

The lab build creates two small nested ESXi hosts with memory tiering ([lab-build requirements](spec/requirements/lab-build.md)). Needed when milestone M4 starts; the author will supply it then.

- **Needs you:** the physical cluster, datastore and network to use, and how much CPU, memory and NVMe space you can spare.

**Answer:**

## Q-122 Licences for the nested hosts

Needed with Q-120.

- **Needs you:** do the lab licences cover two more ESXi hosts?

**Answer:**

## Q-134 PCM's folders by workspace or by phase

PCM's folders follow the phase of work: [spec](https://github.com/e1-rahabok/private-cloud-manager/tree/main/spec), [design](https://github.com/e1-rahabok/private-cloud-manager/tree/main/design), the application code, deploy. One workspace such as L2 is spread over six folders: its design note, its API, catalog and test specifications, its code and its tests. Agent E2 instead groups by subject ([knowledge](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge)), so one folder holds the context of one task. R-REPO-007 renames PCM's folders without moving files between them.

- **Option A, keep the phases:** no move; a session gathers each workspace from six places.
- **Option B, one folder per workspace** (`l2/`, `noc/`, `capacity/`, `docs/`, `executive/`), each with its design, specifications, code and tests, plus one shared folder for the core: one folder is the whole context of a task, at the cost of moving several dozen files and updating every import and path.
- **Recommendation:** B, done after R-REPO-007 and before M6, the first milestone that builds PCM's live demo.

**Answer:**
