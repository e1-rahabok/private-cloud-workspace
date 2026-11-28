# Templates

Empty versions of the files the method produces. Copy them into the root of your parent repository, or of your only repository, and fill them in with your agent: you give the input for the brief, the agent surveys the code and drafts the rest, and you correct its drafts.

| Template | Chapter | Worked example |
|---|---|---|
| [BRIEF.md](BRIEF.md) | [4](../04-goals-and-scope.md), [6](../06-constraints-assumptions-risks-dependencies.md) | [spec/brief.md](../../spec/brief.md) |
| [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) | [5. The interview](../05-the-interview.md) | [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md) |
| [REQUIREMENTS.md](REQUIREMENTS.md) | [7. Requirements](../07-requirements-and-acceptance.md) | [spec/requirements](../../spec/requirements) |
| [DESIGN.md](DESIGN.md) | [3](../03-map.md), [8](../08-design.md), [9](../09-seams-and-owners.md) | [spec/design/system.md](../../spec/design/system.md) |
| [TEST-PLAN.md](TEST-PLAN.md) | [10. Test plan](../10-test-plan-and-traceability.md) | [spec/test-plan.md](../../spec/test-plan.md) |
| [ROADMAP.md](ROADMAP.md) | [12. Slices and sessions](../12-slices-and-sessions.md) | [ROADMAP.md](../../ROADMAP.md) |
| [CLAUDE.md](CLAUDE.md) | [12](../12-slices-and-sessions.md), [13](../13-working-with-the-agent.md) | [CLAUDE.md](../../CLAUDE.md) |
| [GLOSSARY.md](GLOSSARY.md) | [14. Names](../14-names-and-vocabulary.md) | [spec/glossary.md](../../spec/glossary.md) |

A prompt to start with:

> Read every repository listed below. Fill in the Structure, Contracts and Build and test sections of DESIGN.md from what you find, using the templates. Wherever two documents disagree, something is left undecided, or you had to assume something, write a question in OPEN-QUESTIONS.md that asks me for the input you need, with a link to the lines involved and the assumption you will work on until I answer. Do not ask me to choose a design: decide it, write it in DESIGN.md with the options you rejected, and tell me what you decided and why. Do not ask me anything you can work out from the code, the documents or general knowledge of the field.
