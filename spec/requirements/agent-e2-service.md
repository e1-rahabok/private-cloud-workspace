# Requirements: the Agent E2 service

What Agent E2 must do in release 1.0 for its two callers, PCM and isvara.io, and how each part is tested. The service is one Python program, [harness/answer_service.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py). Its HTTP calls are contract [C3, the Agent E2 API](../glossary.md#c3), and its docstring is that contract's specification.

How to read the IDs: "Q-WS-5" is a question of the interview, with the author's answer, in [interview, round 1](../interview-round-1.md). "WD-013" is a decision that binds several repositories, in [DECISIONS.md](../../DECISIONS.md). Every other ID is explained in the [glossary](../glossary.md).

Files involved:

- The service and its settings: [harness/answer_service.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py) and [harness/service_config.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/harness/service_config.yaml).
- The pipeline it runs: [harness/answer_modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_modes.py) (`converse`) and [harness/expert_agent.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/expert_agent.py).
- PCM's client: [build/pcm_proto/agent_e2.py](https://github.com/e1-rahabok/private-cloud-manager/blob/main/build/pcm_proto/agent_e2.py).
- The contract check: [checks/agent_e2_api.py](../../checks/agent_e2_api.py).
- The free-text grader that the answer set reuses, archived since 2026-11-14: [project/archive/legacy/judge-2026-11-14/judge.py](https://github.com/e1-rahabok/agent-e2/blob/ebbc7dc0be3268abc0f4939fe1ea40e400ac9bbb/project/archive/legacy/judge-2026-11-14/judge.py).

## Model and knowledge

### R-E2-001 The service runs Gemma 4 31B through Vercel AI Gateway

Source: WD-013 (Agent E2 in release 1.0: accuracy first, the model, drafts used); answer to Q-WS-7 ("Gemma 4 31B, or later version when it comes"); WD-002 (release 1.0 in the lab, cloud model through the gateway).

- Given the service as deployed for PCM or for isvara.io
- When `GET /v1/health` is called
- Then `model` is `google/gemma-4-31b-it`, or a later Gemma version that has passed the answer set (R-E2-006) first
- And every answer names the same model and the `knowledge_commit` it was written from

Test scenarios:
- T-E2-001a (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py), to extend): read `model` from `/v1/health` and from one answer; both equal the `model` line of [service_config.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/harness/service_config.yaml).
- T-E2-001b (anywhere, manual at each model change): the answer-set report for the new model exists and passes before `service_config.yaml` changes.

### R-E2-002 Every knowledge file is used, drafts included

Source: WD-013; answer to Q-WS-10 ("park this check as after go live. In the meantime, use all files").

- Given the knowledge base at one commit, where most files have `status: draft`
- When the service starts
- Then it loads every Markdown file under [`knowledge/`](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge), whatever its status
- And no answer mentions a file's review status

Test scenarios:
- T-E2-002a (anywhere, automated by [harness/test_harness.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/test_harness.py), to build): `files` in `/v1/health` equals the number of Markdown files under [`knowledge/`](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge), counted with the loader in [harness/knowledge_loader.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/knowledge_loader.py).
- T-E2-002b (anywhere, automated by the answer-set grader of R-E2-005): no answer in the answer-set report contains "draft", "reviewed" or "review status".

### R-E2-003 Agent E2 looks nothing up on the web

Source: answer to Q-WS-47 ("The docs look up is not applicable for Agent E2").

- Given a question from PCM or isvara.io, with or without a link in its text
- When Agent E2 answers
- Then it makes no web search and fetches no page
- And when the question carries a link, the answer says Agent E2 cannot open pages and answers from the knowledge base

Test scenarios:
- T-E2-003a (anywhere, automated by [harness/test_harness.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/test_harness.py), to build): with `web.enabled: false` from `service_config.yaml`, a question holding `https://knowledge.broadcom.com/...` calls no function of [public_web_lookup.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/public_web_lookup.py) (patched to fail if called).
- T-E2-003b (anywhere, automated by the answer-set grader of R-E2-005): one answer-set question holds a link; its key point is that the page was not opened.

## Answer quality

### R-E2-004 An answer set of free-text questions for release 1.0 exists

Source: WD-013; answers to Q-WS-5 ("The grader should be automated") and Q-WS-I1 (conversations, CSV files and screenshots); WD-012 (release 1.0 success: Agent E2 explains a real lab KPI correctly); the author, 2026-11-27 (about 15 questions in release 1.0, since the grader has lower priority; more questions after 1.0).

- Given the questions PCM users and isvara.io readers ask
- When the answer set is read
- Then it holds at least 15 free-text questions: at least 3 on PCM's synthetic ACME screens with their facts, 2 on the live demo with facts recorded from the lab, 5 for isvara.io readers with no facts, 2 with a CSV file, 2 with a screenshot, and 1 that continues a conversation of two or more turns
- And each question has its expected key points, its likely wrong answer, and the knowledge files that hold the answer
- And no question copies the wording of a multiple-choice benchmark question

Test scenarios:
- T-E2-004a (anywhere, automated by `benchmark/runner/answer_grader.py`, to build in agent-e2): count the questions by kind in `benchmark/answer-set/`; fail when a kind is short or a question lacks a key-point list, a likely wrong answer or a knowledge id that exists.
- T-E2-004b (anywhere, automated by the same tool): no answer-set question shares a run of 12 or more words with any file in [benchmark/questions/](https://github.com/e1-rahabok/agent-e2/tree/main/benchmark/questions).

### R-E2-005 An automated grader scores every answer

Source: answer to Q-WS-5 ("It was graded by Opus 5.5"); WD-013.

- Given an answer to an answer-set question
- When the grader reads it
- Then Claude Opus 5.5 (`anthropic/claude-opus-5.5`, temperature 0) scores it 0 to 3 by the rubric of the archived judge: 0 wrong, or the likely wrong answer, or a contradicted key point; 1 the conclusion avoids the trap but the reason is missing or wrong; 2 right conclusion with the right reason; 3 as 2, and every key point or what to check next
- And it also marks whether the answer states the likely wrong answer (misconception) and whether it says the question is not settled (unsure)
- And it sees what Agent E2 saw: the question, the facts, the conversation, the CSV text and the screenshots
- And an answer that asked a clarifying question is scored on its final answer after the scripted reply

Test scenarios:
- T-E2-005a (anywhere, automated by `benchmark/runner/answer_grader.py`, to build, with the mock client of [harness/model_client.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/model_client.py)): a reply that is not valid JSON gets one retry, then fails the grading with the reply's first 200 characters; a valid reply gives score, misconception, unsure, missed and reason.
- T-E2-005b (anywhere, automated, to build): for a question with a screenshot, the grader's request holds the image; for a question with a CSV, the CSV text.
- T-E2-005c (anywhere, manual once): the author grades 20 answers picked at random; the grader agrees with the author on right (2 or 3) against not right (0 or 1) for at least 17 of them. Below that, the rubric is fixed and the 20 are graded again.

### R-E2-006 The answer set passes on the shipped configuration

Source: WD-013; answers to Q-WS-5 and Q-WS-I3 ("Accuracy matters more"); WD-012.

- Given the service with its shipped `service_config.yaml`
- When every answer-set question is answered 3 times and graded
- Then the mean credit (score divided by 3) is at least 0.75
- And at most 5% of the answers are confidently wrong (score 0 and not marked unsure)
- And no answer is marked as stating a misconception
- And each live-demo question has a mean credit of at least 0.67
- And the report records, per answer: the score, the model, the knowledge commit, the time taken and the tokens used

Test scenarios:
- T-E2-006a (anywhere with the gateway key, automated by `benchmark/runner/answer_grader.py`, to build): run the set; write `benchmark/results/answer-set-<date>/report.md`; exit 1 when any limit is missed. The run stays within the US$100 benchmark budget of WD-014 (gateway spending).
- T-E2-006b (anywhere, manual): rerun after every change of model, of a prompt in [`harness/`](https://github.com/e1-rahabok/agent-e2/tree/main/harness), or of `service_config.yaml`, and before each roadmap milestone that ships Agent E2 is closed.

## Time and progress

### R-E2-007 A caller can follow a long answer while it is written

Source: WD-013 ("an answer may take minutes; no streaming, but the user always sees that Agent E2 is still working"); answer to Q-WS-I3 ("how to inform user Agent E2 is not hung or dead?").

- Given a caller that sends `POST /v1/answer` with `"async": true`
- When the service accepts it
- Then it replies at once with HTTP 202 and `{"job": "<id>", "state": "queued"}`
- And `GET /v1/jobs/<id>` returns `state` (queued, running, done or failed), `stage` (one of topic, shape, understand, plan, compute, write, check, rewrite), `elapsed_s` and `updated_at`
- And while the job is queued or running, `updated_at` changes at least every 10 seconds, also during a long model call
- And when the job is done, the reply holds `result`, the same object a synchronous `/v1/answer` returns

Test scenarios:
- T-E2-007a (anywhere, automated by [harness/test_harness.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/test_harness.py), to build): a mock client that sleeps 35 seconds in the answer call; poll every 2 seconds; expect the stages in pipeline order, `updated_at` never older than 10 seconds, and `result` at the end.
- T-E2-007b (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py), to extend): the job reply has every field above with its type; `result` passes the same field check as `/v1/answer`.

### R-E2-008 A stuck or failed answer ends with a reason

Source: WD-013; answer to Q-WS-I3.

- Given a job whose model call fails, or which runs longer than 10 minutes
- When the caller polls it
- Then `state` is `failed` with `error.reason` set to `model_error` or `time_limit`, and a sentence a person can read
- And no job stays running for more than 10 minutes
- And a finished or failed job can be read for 15 minutes, then returns HTTP 404

Test scenarios:
- T-E2-008a (anywhere, automated by [harness/test_harness.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/test_harness.py), to build): a mock client that raises `LLMError`; expect `failed` and `model_error`.
- T-E2-008b (anywhere, automated, to build): a time limit of 3 seconds set for the test and a mock client that sleeps 5 seconds; expect `failed` and `time_limit`.

### R-E2-020 A caller reads a job every 10 seconds

Source: WD-013 ("the user always sees that Agent E2 is still working"); answer to Q-WS-I3 ("how to inform user Agent E2 is not hung or dead?"); the author, 2026-11-27 ("VMware Admin does not mind 10 seconds waiting as he knows this is not a general chat").

- Given PCM or isvara.io waiting on an Agent E2 job (R-E2-007)
- When the job is queued or running
- Then the caller reads `GET /v1/jobs/<id>` once every 10 seconds, and not more often
- And between reads, the time so far counts up every second in the browser, with no call to Agent E2
- And the screen shows the current stage as words a person reads, never the stage's code name
- And when `updated_at` is more than 60 seconds old, the screen says that Agent E2 is not responding and offers to try again
- And when the job fails, the screen shows the reason of R-E2-008; when Agent E2 cannot be reached, it says that Agent E2 is unavailable

Test scenarios:
- T-E2-020a (anywhere, automated in private-cloud-manager by `build/tests/agent_e2_job.test.mjs`, to write): a fake job endpoint that counts requests and runs a job for 60 seconds; expect at most 7 reads, the stage in words, and the answer at the end.
- T-E2-020b (anywhere, the same test): the fake stops changing `updated_at`; expect "not responding" on screen within 70 seconds.
- T-E2-020c (anywhere, automated in isvara by Ask Agent E2's tests, to write in M8): T-E2-020a and T-E2-020b on Ask Agent E2.

### R-E2-009 The synchronous call keeps working until both callers have moved

Source: WD-010 (every contract has a check; changes go expand, migrate, contract); WD-013.

- Given PCM's client, which calls `/v1/answer` and waits up to 180 seconds ([agent_e2.py](https://github.com/e1-rahabok/private-cloud-manager/blob/main/build/pcm_proto/agent_e2.py#L105))
- When the job calls of R-E2-007 are added
- Then a call without `"async"` still returns the answer in one reply, with every field it has today
- And PCM and isvara.io each move to the job calls in their own pull request before the synchronous form is removed

Test scenarios:
- T-E2-009a (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py)): the check as it runs today, through PCM's client, passes after the job calls are added.

### R-E2-010 Each answer reports its time and use

Source: WD-013; WD-014 (gateway spending: US$100 per benchmark run, US$50 a month after isvara.io goes live); answer to Q-WS-9.

- Given any answer
- When it is returned
- Then it holds `elapsed_s`, the seconds per stage, and `usage`: the number of model calls, prompt tokens and completion tokens.

Test scenarios:
- T-E2-010a (anywhere, automated by [harness/test_harness.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/test_harness.py), to build): with a mock client that reports 100 prompt and 20 completion tokens per call, `usage` equals the sum over the calls the trace records.
- T-E2-010b (anywhere, automated by `benchmark/runner/answer_grader.py`): the answer-set report gives the median per answer.

## Conversations, CSV files and screenshots

### R-E2-011 A conversation continues over several turns

Source: answer to Q-WS-I1 ("Agent E2 is capable of answering back, forming a chat back and forth").

- Given a caller that sends the earlier turns of the current topic in `history`, and the clarifying round in `turns`
- When it asks a follow-up question
- Then Agent E2 decides whether the question continues the topic and reports it in `topic`
- And it asks at most one round of clarifying questions (`type: clarify`), then answers

Test scenarios:
- T-E2-011a (anywhere, automated by [harness/test_harness.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/test_harness.py) and [benchmark/runner/topic_check.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/topic_check.py)): the existing conversation and topic tests pass.
- T-E2-011b (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py), to extend): an isvara.io-shaped call with two earlier turns and no facts returns `topic` with `continues` and `by`.

### R-E2-012 Agent E2 reads screenshots a caller sends

Source: answer to Q-WS-I1 ("Agent E2 is capable of accepting CSV file and VMware screenshots").

- Given a call to `/v1/answer` with `attachments` holding up to 5 images (PNG, JPEG or WebP, base64, each at most 5 MB)
- When Agent E2 answers
- Then the images reach the model in the understand stage and in the answer stage, as they do in the benchmark today
- And the reply lists, per image, what was read from it (tool, object, metric names, values, units, interval) in `attachments_read`

Test scenarios:
- T-E2-012a (anywhere, automated by [harness/test_harness.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/test_harness.py), to build): a mock client records its messages; a call with one PNG shows an `image_url` part in both the understand and the answer request. Today the service passes no images ([answer_service.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py#L470)).
- T-E2-012b (anywhere with the gateway key, automated by the answer-set grader): the 4 screenshot questions of the answer set pass.

### R-E2-013 Agent E2 reads CSV files a caller sends

Source: answer to Q-WS-I1.

- Given a call to `/v1/answer` with `attachments` holding up to 3 CSV files, at most 200 KB of text in all
- When Agent E2 answers
- Then each file reaches the model as text under its file name, as the benchmark runner sends CSV attachments today ([question_files.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/question_files.py#L108))
- And the answer's figures from the file are the file's own values

Test scenarios:
- T-E2-013a (anywhere, automated by [harness/test_harness.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/test_harness.py), to build): a mock client records its messages; a call with `vm-cpu.csv` shows the file name and its rows in the answer request.
- T-E2-013b (anywhere with the gateway key, automated by the answer-set grader): the 4 CSV questions of the answer set pass.

### R-E2-014 An attachment that cannot be read is refused, never dropped

Source: answer to Q-WS-I1.

- Given a call with an attachment of another type, above the size limits, or that does not decode
- When the service receives it
- Then it answers HTTP 400 with the attachment's name and the reason, and calls no model

Test scenarios:
- T-E2-014a (anywhere, automated by [harness/test_harness.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/test_harness.py), to build): one call each with a PDF, a 6 MB PNG, 4 CSV files and broken base64; expect 400 and no model call in the mock's log.

## The two callers

### R-E2-015 A call without page facts gets a general answer

Source: WD-004 (PCM and isvara.io both use Agent E2; Agent E2 replaces AskIO); answer to Q-WS-I5 (isvara.io for VMware administrators and architects).

- Given a call with a question and no `facts`, as isvara.io sends
- When Agent E2 answers
- Then the answer uses no PCM screen rule: it names no PCM page, tab, chart or Sources list, and has no opening (`lead` is empty)

Test scenarios:
- T-E2-015a (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py), to extend): an isvara.io-shaped call returns every field of the answer with its type, and an empty `lead`.
- T-E2-015b (anywhere with the gateway key, automated by the answer-set grader): no reader answer in the report contains "PCM", "this page" or "the tab".

### R-E2-016 Every answer lists the knowledge files it used, by ID and title

Source: answer to Q-WS-45 ("User must be able to click on the cited page"); WD-017 (isvara.io rebuilt; a cited source opens the knowledge file, with a note that it is written for a model).

- Given any answer
- When it is returned
- Then `sources` lists each knowledge file the answer used, with its `id` (its path under [`knowledge/`](https://github.com/e1-rahabok/agent-e2/tree/main/knowledge) without `.md`) and its `title`
- And each `id` is a file that exists at the answer's `knowledge_commit`
- And the answer text itself holds no file ID or path

Test scenarios:
- T-E2-016a (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py), to extend): every `sources` id resolves to `knowledge/<id>.md` in the agent-e2 clone; every title equals that file's first heading.
- T-E2-016b (anywhere, automated by [harness/test_harness.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/test_harness.py)): the existing `no_file_refs` tests pass.

## Facts PCM sends

### R-E2-017 The specification lists the facts each answer feature needs

Source: answer to Q-WS-36 ("agree": C3's specification lists the facts each feature needs; C3's check adds a live-shaped case; Agent E2 says when a needed fact is missing).

- Given the docstring of [answer_service.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/answer_service.py), the specification of the Agent E2 API
- When it is read
- Then it has one table: each feature, the facts it needs, and what Agent E2 does without them
- And the table starts from these features, with the fact names PCM sends today ([frame.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/spec/workspaces/l2/frame.md)):

| Feature | Facts it needs | Without them |
|---|---|---|
| The opening on how a score moved (`lead`) | `kpis`: `label`, `better`, `points` | No opening |
| When a score changed level, and which parts moved | `kpis` points over at least 2 hours; `parts_hourly` for the parts | No step line; no parts named |
| The part that pulled a score down at its worst point | `asked_about_kpi.parts_at_worst` | No part named |
| The capacity opening (close for business) | `pillar: Capacity`; `check` (the Periodic Cluster Check values) or the Consumption, Performance and Risk series; `production` | No capacity opening |
| The band of each figure on the screen | each metric's name, as in the catalog, and its value | No band line |
| Where to look next | `screen.drill_down` | No pointer |
| Suggested questions | `object.kind`, `pillar`, `kpis` | No suggestion |

Test scenarios:
- T-E2-017a (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py), to extend): parse the table from the docstring; every fact name in it appears in PCM's frame.md; every feature has a row.

### R-E2-018 A missing fact is said, never guessed

Source: answer to Q-WS-36; WD-015 (PCM's live demo shows what the VCF vCommunity Adapter publishes and says "No data" when a value is stale).

- Given a live-demo call whose facts lack a fact a feature needs (for example no `parts_hourly`, or a part whose value is "No data")
- When Agent E2 answers
- Then the reply lists the missing facts in `missing_facts`
- And the answer says in one sentence what the page did not supply, and gives no value for it

Test scenarios:
- T-E2-018a (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py), to extend): a live-shaped fixture, recorded from the lab and stripped of `parts_hourly`, returns `missing_facts` holding `parts_hourly`.
- T-E2-018b (lab, automated by the answer-set grader): the 5 live-demo questions run on facts recorded from the lab VCF Operations; their key points include what the page did not supply.

## The contract check

### R-E2-019 The contract check covers both callers and every new field

Source: WD-010; answer to Q-WS-I1 ("I expect you to check all the contracts").

- Given the Agent E2 service in mock mode (no model, no network)
- When [checks/agent_e2_api.py](../../checks/agent_e2_api.py) runs
- Then it calls the service as PCM does, through PCM's client, and as isvara.io does: until isvara.io has its own client, with a call the check builds from the specification
- And it checks the fields of R-E2-007, R-E2-010, R-E2-012, R-E2-016 and R-E2-018 by name and type

Test scenarios:
- T-E2-019a (anywhere, automated by [checks/agent_e2_api.py](../../checks/agent_e2_api.py), to extend): the check passes on agent-e2's main branch.
- T-E2-019b (anywhere, manual once per new field): remove the field in a copy of the service; the check fails and names it.

## Not in this file

- The injection guard and the limits on public use belong to isvara.io, before it calls Agent E2 (answer to Q-WS-47; WD-017). They go in `isvara-agent.md`.
- Where the public Agent E2 runs is decided after measuring start-up time and cost per question (answer to Q-WS-4).
- Keeping gateway spending within US$50 a month after isvara.io goes live is a task for after go-live (WD-014). `usage` in R-E2-010 gives the numbers it needs.

## Questions for round two

The questions on this file, with their decisions, are in the [interview, round 2](../interview-round-2.md): Q-WS-90 to Q-WS-99 (and Q-WS-57, Q-WS-61, Q-WS-62). The few still open are in [OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md).
