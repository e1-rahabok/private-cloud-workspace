# Requirements: knowledge content for isvara.io

Contract [C4, knowledge content for isvara.io](../glossary.md#c4): what Agent E2's export gives isvara.io to build its pages from. Agent E2 writes the export ([knowledge-export.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/requirements/knowledge-export.md) in agent-e2); isvara.io reads it at a pinned commit; the workspace keeps the schema both sides check against, and the check of the export ([WD-036](../../DECISIONS.md)). These requirements belong to milestone M4 in [ROADMAP.md](../../ROADMAP.md). Other IDs are explained in the [glossary](../glossary.md).

### R-EXPORT-001 One schema for the export, checked on both sides

Source: answer to Q-WS-41 (the export, with a check that every link and image resolves); WD-010 (every contract has a check); WD-036.

- Given the export schema in this workspace, `checks/knowledge_export_schema.json`
- When the cross-repo checks run
- Then `checks/knowledge_export.py` runs agent-e2's export tool on the agent-e2 clone and validates the result against the schema
- And isvara.io's build validates the export it reads against the same schema and stops on any difference

Test scenarios:
- T-EXPORT-001a (anywhere, automated by `checks/knowledge_export.py`, to write, run by [`checks/run_all.py`](../../checks/run_all.py)): the export of agent-e2's main passes; a copy with one record missing its `internal_derive` field fails and names the record.
- T-EXPORT-001b (anywhere, automated by isvara's article check of R-CONTENT-016, to write): a fixture export without `fingerprint` stops the build.

### R-EXPORT-002 isvara.io reads only what the schema names

Source: WD-001 (isvara.io holds no knowledge of its own); WD-005.

- Given isvara.io's build
- When it reads Agent E2's knowledge
- Then it reads only the export, and only fields the schema names

Test scenarios:
- T-EXPORT-002a (anywhere, automated by isvara's article check, to write): a build whose code reads a field missing from the schema fails and names the field.
