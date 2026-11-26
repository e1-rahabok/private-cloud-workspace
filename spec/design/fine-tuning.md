# Fine-tuning the model: design note

**Status:** for the author's review. Written in answer to the author's comment in [intent.md](../intent.md): "why do we need to fine tune a model? Document the pros and cons on a separate design document … Provide recommendation".

**Short answer:** fine-tuning is not needed for stage 1, and it would break the stage 1 set-up. The current approach puts the knowledge in files that Agent E2 reads at answer time. It keeps every fact current, cited and checkable. Fine-tuning becomes worth a measured trial only if the answer set shows a failure that comes from the model's own behaviour and that no prompt or knowledge fix removes.

## Origin of the rule

Agent E2 lists fine-tuning under Not doing in its plan ([project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md#L209)): "Facts change and must be cited; retrieval supplies them". Its architecture gives four reasons ([ARCHITECTURE.md](https://github.com/e1-rahabok/agent-e2/blob/main/ARCHITECTURE.md#L321)): the knowledge is not on the Internet, it changes often, answers must cite files, and small models memorise facts poorly. It leaves one door open: "a light fine-tune (LoRA) for style and terminology only" ([ARCHITECTURE.md](https://github.com/e1-rahabok/agent-e2/blob/main/ARCHITECTURE.md#L322)). The mission states that the model "is not a customized or fine-tuned model" ([MISSION.md](https://github.com/e1-rahabok/agent-e2/blob/main/MISSION.md#L12)).

Nothing was measured to reach this. It was a design call. This note weighs it again.

## Agent E2 today

- **The model is frozen.** Gemma 4 31B with open weights, the stage 1 model ([W-013](../../DECISIONS.md), Agent E2 in stage 1). Nobody changes its weights.
- **The knowledge reaches the model at answer time.** For each question, agent code picks up to 32,000 tokens of knowledge files (the reading set), looks up exact values in the catalog, computes figures with a calculator, and puts the misconceptions that matter most at the top of every prompt ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)). The model reads and writes; code decides what it reads.
- **One fact has one home.** A change to a knowledge file reaches the next answer, with no training step. The answer cites the files it used, and the person can open them ([W-017](../../DECISIONS.md), the isvara.io rebuild).

## Fine-tuning in this setting

Fine-tuning trains the model further on examples, so that its weights hold new behaviour or new facts. For a 31-billion-parameter model the practical form is a LoRA adapter: a small set of extra weights (around 1% of the model's size) trained on top of the frozen model and loaded with it at answer time. It can be trained for three things:

- **Facts.** Trained on the knowledge files as text to learn. The model would "know" the knowledge base without reading it. This is the kind the "not done" rule is about.
- **Behaviour.** Trained on example questions with model answers: the answer shape, Level 400 reasoning, saying unsure, citing files, setting aside the Internet's rules of thumb. The facts still come from the reading set. This is the door ARCHITECTURE.md leaves open.
- **Preference.** Trained on pairs of a good and a bad answer to the same question. It changes which answer the model leans to, mostly tone and safety.

## Pros and cons against the current approach

- **A fact changes.**
  - Today: the file changes, and the next answer uses it.
  - Fine-tuned: a trained fact stays until the next training run. The knowledge base changes daily (11 flow files on 2026-11-25 alone).
- **Citations.**
  - Today: each answer names the files it read, and the person can check them (Q-45, isvara.io citations).
  - Fine-tuned: a trained fact has no file behind it, so the answer cannot say where it came from.
- **A wrong answer.**
  - Today: the trace shows what was read, and the fix is one file.
  - Fine-tuned: the cause can be in the weights, and the fix is new examples and a new training run.
- **The Internet's rules of thumb,** such as "Ready above 5% is bad".
  - Today: the correction is put in front of the model with every question, but the model can still lean to its old belief (prior override, [models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md#L23)).
  - Fine-tuned: behaviour training can weaken the old belief. This is the strongest argument for it.
- **Answer style and shape.**
  - Today: set by prompt rules and code.
  - Fine-tuned: can be trained in, so prompts get shorter.
- **A later Gemma version** (Q-7: "or later version when it comes").
  - Today: change one line in the settings and rerun the answer set.
  - Fine-tuned: every adapter is tied to one model version, so a new version needs new training.
- **Hosting in stage 1.**
  - Today: Vercel AI Gateway serves Gemma 4 31B from its providers ([C5, the model gateway](../glossary.md#c5)).
  - Fine-tuned: as far as is known, the gateway serves only the providers' own models, not your own weights or adapter (to verify before any trial). A fine-tuned model needs its own GPU endpoint.
- **Cost per answer.**
  - Today: per token, through the gateway. The round of 2026-11-16 cost US$8.27 for 2,910 Gemma answers ([benchmark/results/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/README.md)).
  - Fine-tuned: its own GPU endpoint costs money every hour it runs, whether or not anyone asks.
- **Proof.**
  - Today: the benchmark and the answer set test the whole system on a frozen model.
  - Fine-tuned: each adapter version needs its own runs, and the claim "a standard model" changes.

## Evidence on the model

The model is not where most errors come from. In the multiple-choice rounds, a model that had every needed file in front of it lost very few points: Muse lost 1.7 of its 22 lost points that way ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md#L31)), and in the last round the model lost under 2 points with every needed file read ([project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md#L316)). Most errors were files the reading set missed, or facts no file held. Training fixes neither.

Free-text answers are a different matter and are not measured yet. The answer set of [R-E2-004 to R-E2-006](../requirements/agent-e2-service.md) will show, for the first time, how often Gemma writes a wrong free-text answer with the right files in front of it.

## Cost

These are estimates, not quotes. Prices change; check them before any trial.

- **Training data.** Claude drafts 1,000 to 3,000 examples from the knowledge base, and a review agent checks each one: tens of US dollars in model calls. Each example needs a question, the files it rests on, and a correct answer at Level 400.
- **The author's review.** The real cost: at least 100 sampled examples, read by the author. A wrong example teaches a wrong habit to every answer, and the author has no time to review files one by one (Q-10).
- **Training.** A few hours on one rented 80 GB GPU per run, at a few US dollars an hour, and several runs to settle the settings: tens of US dollars per round of trials.
- **Hosting.** One GPU endpoint running all day costs hundreds of US dollars a month or more. One that starts on demand is cheaper, but its first answer waits for the model to load. The gateway cannot serve it.
- **Upkeep.** One more training run for each new Gemma version, and for each large change to the behaviour wanted, since adapters do not carry across model versions.

The budget after isvara.io goes live is US$50 a month for the gateway, on top of the US$40 Vercel subscription ([W-014](../../DECISIONS.md), gateway spending). A dedicated GPU endpoint alone would exceed it.

## Data needed

- **For behaviour training:** 1,000 to 3,000 examples, spread over the kinds of question Agent E2 meets: metric meaning, how it works, what to set, troubleshooting, decision trees, capacity, the PCM screens, CSV files and screenshots. Each answer is grounded in named knowledge files, says unsure where the files do not settle the question, and follows the answer shapes.
- **Kept apart:** no example may copy or paraphrase a benchmark question or an answer-set question. Otherwise the tests would measure memory of the test.
- **Versioned:** each example names the knowledge commit it was written from. Examples on a changed file are rewritten before the next training run.
- **For fact training:** the knowledge files themselves. Not recommended, for the reasons above.

## Effect on the benchmark

- **The claim changes.** Today the claim is that a standard open-weight model, with this agent, harness and knowledge base, answers better than a frontier model ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md#L7)). A fine-tuned model makes it "our own trained model", a weaker story for customers who want to fork and run it on their own models (W-012, stage 1 success).
- **More runs.** Each round would need the base model, Agent E2, and Agent E2 with the adapter, to show what the training adds.
- **Leakage risk.** The examples come from the same knowledge base the questions test. That is fair as long as no example repeats a question; a check would compare every example with every question, as T-E2-004b does for the answer set.

## Effect on stage 2

Stage 2 is the customer's own deployment with a local model, out of scope now ([W-002](../../DECISIONS.md), stage 1 only). There, an adapter is easier: a local vLLM server can load LoRA adapters next to the base model, and the adapter could ship in the offline bundle with the knowledge. Two limits stay: the adapter is tied to one model version, and customers who pick another open model would get no adapter. Training on a customer's own data is a separate question, with privacy concerns, and is not proposed.

## Recommendation

1. **No fine-tuning in stage 1.** Hosting alone rules it out: the gateway serves no custom model, and a GPU endpoint would exceed the US$50 a month. The frozen model with the knowledge base keeps facts current and cited, and the evidence puts most errors in retrieval and knowledge, not in the model.
2. **Keep the row under Not doing in Agent E2's plan, and point it at this note.** Reword it: "Fine-tuning: not in stage 1; see the workspace design note", and keep the ARCHITECTURE.md line on a light LoRA for behaviour as the stage 2 option.
3. **Revisit on a measured trigger.** The trigger: after the answer set has run, its traces show a recurring wrong free-text answer where the right files were in the reading set, and two rounds of prompt or knowledge fixes did not remove it. Then run one trial: a behaviour adapter on Gemma 4 31B, about 1,000 examples, measured on the answer set against the frozen model. Keep it only if it gains outside the margin.
4. **Never train facts into the model.** Facts stay in the knowledge base, where they can be cited, checked and changed.
