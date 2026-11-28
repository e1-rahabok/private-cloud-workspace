# 8. Design

## Purpose

Requirements say what the product must do. The design says how the parts will do it within the constraints, and why this way. It is the architect's document, so in this method the agent writes it. The person reads it for two reasons: to catch a mistake about the domain that the agent cannot see, and to learn how the system works, so that later answers and reviews are better informed.

In this project the workspace's design is [spec/design/system.md](../spec/design/system.md). Each repository keeps the design of its own inside, such as PCM's [core design note](https://github.com/e1-rahabok/private-cloud-manager/blob/main/pcm/core/design-notes/pcm-core.md) and Agent E2's [ARCHITECTURE.md](https://github.com/e1-rahabok/agent-e2/blob/main/ARCHITECTURE.md). The examples in this chapter come from all three.

## Contents of a design

- **Context:** the goals, constraints and requirements the design answers, by ID.
- **Structure:** the parts, where each runs, and what data flows between them ([chapter 3](03-map.md)).
- **Contracts:** where the parts meet and who owns each shape ([chapter 9](09-seams-and-owners.md)).
- **Quality attributes:** security, scalability, performance, reliability, maintainability, testability and cost, each with its target and the mechanisms that meet it.
- **Choices:** each significant choice, with the options it rejected and the reasons.
- **Risks and deferrals:** what the design depends on that is not yet known, and which choices wait for it.

## A design choice, written out

A choice is worth writing down when a reasonable person could have chosen otherwise. Each one has the same fields, and an ID such as DESIGN-3 so that a test or a requirement can cite it:

- **Context:** the problem, and the constraints that bear on it.
- **Options:** the realistic ones, including the one a newcomer would try first.
- **Choice:** the option taken.
- **Reasons:** why it wins, and why each other option loses.
- **Consequences:** what the choice costs, and what it rules out.
- **Serves:** the goals, requirements and constraints it answers.

Agent E2 chose how its model gets its facts, and the choice reads well in this form ([ARCHITECTURE.md](https://github.com/e1-rahabok/agent-e2/blob/main/ARCHITECTURE.md), section 8):

- **Context:** a small model on the customer's own GPU; knowledge that is on no public website and changes often; every answer must cite its files.
- **Options:** train the facts into the model; put the whole knowledge base into every prompt; a graph database; retrieve the relevant files for each question.
- **Choice:** retrieval.
- **Reasons:** small models memorise facts poorly, and a trained model would need retraining at every change. The whole knowledge base is about 315,000 tokens, too much for a small model and too slow per question. A graph database would hold what the links between the knowledge files already form.
- **Consequences:** an answer is only as good as the files retrieval finds, so every change to the structure needs a before and after number from the retrieval check.
- **Serves:** accurate before complete; the customer's data stays on site; every answer cites its source.

The workspace's [system design](../spec/design/system.md) writes the same fields in a shorter form: a title and the choice, then Why, Rejected and Serves. DESIGN-17, "Missing data never shown as a value", says that the adapter "publishes no value built from a partial read" and that PCM shows "No data" for a stale value. Why: "a partial read gives values that look normal, which is a correctness bug, and a blank is honest". Rejected: state codes in release 1.0, and a 15-minute wait before a value counts as stale, since "the author asked for no wait". Serves: PRINCIPLE-2, SCOPE-5 and four requirements. The context is in the IDs it serves, and the consequences are in the requirements that cite it.

## Same problem, other constraints

isvara.io answered questions about the same books with the opposite design. It put the whole Book, about 327,000 tokens, into a large cloud model's context on every request, with no search at all, and kept the fixed part of the prompt first so the provider could reuse it from its cache. With a large model, a cache and a small budget per question, that was the simplest design that worked.

Neither design is wrong. Each one is right for its constraints, and the reasons say which constraint decided it. When isvara.io moves onto Agent E2 in release 1.0, its constraints change, and its design changes with them: the whole-Book prompt retires. A design choice with its reasons written down can be revisited the day its constraints move; one without them gets defended or copied.

## Quality attributes

A quality attribute starts as a quality requirement with a target ([chapter 7](07-requirements-and-acceptance.md)), and the design adds the mechanisms that meet it. The examples below come from this project's designs.

### Security

Start with a short threat model: what is worth protecting, who might attack it, and where they could get in. Each mechanism should name the threat it blocks.

- **Least privilege.** PCM's users never log in to vCenter through PCM; only PCM's service accounts reach the source systems, and the role a person has decides what they see and do ([pcm-core.md](https://github.com/e1-rahabok/private-cloud-manager/blob/main/pcm/core/design-notes/pcm-core.md), section 3.10). The adapter's tools read and validate with a read-only account, and only installing uses the admin account.
- **No hidden access.** Agent E2 reads and acts only through PCM's API, with the permissions of the person it acts for, so every action can name a person (section 3.12).
- **Data leaves only by rule.** When Agent E2 searches the web for current facts, its query drops words that look like the customer's system names, so the names of VMs, hosts and datastores stay on site. It refuses private and local network addresses, so a crafted link cannot reach the customer's internal systems, and it treats every fetched page as untrusted text.
- **Instructions hidden in a question.** isvara.io will check each visitor's question with one small model call before Agent E2 sees it, and a flagged question gets a fixed reply (DESIGN-10).
- **Secrets.** The agent never sees a password. On the author's laptop, credentials are encrypted files that only the author's Windows account can open; on the lab's virtual machine they sit in a file that only root and the `pcm` group can read (DESIGN-9).

### Scalability

Size the design with numbers before choosing a mechanism. PCM's core design counts what a large customer means: 100,000 VMs × 20 metrics × 288 five-minute intervals a day is about 576 million points a day (section 3.3). From that number follow three choices:

- **A curated set of metrics.** The models need about 20 metrics per VM, so PCM stores those and nothing else.
- **Detail on demand.** Per-second data and per-disk metrics are fetched from the source when an engineer opens an investigation, and never stored for every object (section 3.4).
- **No collectors of its own.** PCM reads through each region's VCF Operations, which already collects there. A second collector would double the API load on every vCenter and add a component to install, patch and secure in every region (section 3.9).

Agent E2 makes the same move for its automated health check: tens of millions of metrics cannot pass through any model, so code scores them against the threshold catalog, and the model reads only the objects in red or orange.

### Performance

The target comes from the requirement, and the requirement from the person's knowledge of the users. Agent E2 puts accuracy before speed, so an answer may take minutes. The design follows: no streaming of a half-finished answer; the caller starts a job, reads its state every 10 seconds, and counts the elapsed time up in the browser between reads, so the screen moves every second without a call. The 10 seconds came from the author's input that a VMware administrator "does not mind 10 seconds waiting" (DESIGN-14, ASSUMPTION-2).

### Reliability

- **Every number carries its age.** Each value in PCM's API carries its source, its time and the version of its definition, and a value older than two collection cycles shows grey. The design note gives the reason in one line: "The most dangerous screen is green because it is blind" (section 3.5).
- **No value from a partial read.** When one batch of objects fails to read, the adapter publishes nothing for the rows built from it, since a worst-VM value computed from half the VMs looks normal and is wrong (DESIGN-17).
- **A circuit breaker per source.** After repeated failures PCM stops calling one VCF Operations instance for a while and marks its data stale, so one slow region does not slow every screen (section 3.9).
- **PCM watches itself.** Once the operations centre runs on PCM, an outage of PCM must never look like a quiet night, so its own health is on its wall (section 3.11).

### Maintainability

- **One number, one definition, one place.** Every KPI and threshold is defined once, and every other copy is generated from it or checked against it (section 1; DESIGN-2 in the workspace). The contract check of [chapter 11](11-checks.md) is this principle in code.
- **The specification is the source.** AI generates the code from the specification, and people maintain the specification, so a change starts in the specification.
- **Plain technology for the prototype.** PCM's prototype uses Python's standard library, plain HTML and JavaScript, with no framework and no build step. The choice covers the prototype only; the product's technology waits for the facts, as the next section shows.

### Testability

PCM's prototype serves synthetic data, ACME Corp, a made-up global bank, through the same API contract that live data will fill later. The expected numbers are known in advance, so every regeneration of the code is checked automatically, and switching to the lab replaces only the collection layer (section 3.13).

### Cost

Model spending has a monthly limit ([chapter 6](06-constraints-assumptions-risks-dependencies.md)). The design spends model calls only where judgement is needed: code does the scoring, the counting and the parsing of CSV files, and the model explains. A daily ceiling on model calls and question limits per address keep the month inside the budget (DESIGN-20).

## Choices made late on purpose

Some choices are better made later, once the facts exist. PCM's design defers its database, language and user interface framework until a check on the live system shows the real data volumes (section 5). It records what the choice waits for and the rule it will follow: "boring, proven, easy for AI to generate and for customers to run on premises". Written this way, the deferral is itself a decision: it names the fact it waits for. Choosing the database before the volumes are known would have meant guessing them.

## The home of a design choice

A choice is written in the design, beside the part it shapes, and nowhere else. PCM's design note began with "Decisions proposed here move to decisions.md once accepted", which kept every accepted choice in two files. In the workspace, with its decision log retired, the system design is the one home of a design choice, and git records when each choice changed and why. PCM still keeps its own decisions.md.

## The person's part

The architect cannot design without the expert. PCM's storage keeps "the 20-second peak" of each 5-minute interval, and hourly rollups that keep the maximum and the 95th percentile, because "a few seconds of spike vanish in 300 seconds of average". That is the author's domain knowledge, from the SP5 framework the author teaches, turned into a storage design. The agent could not have chosen it alone, and the author would not have written the retention table. Reading the design is how the person catches the place where the agent misread the domain, and how the person learns the parts of the system they will later be asked about.

## In VMware terms

A VMware design document records each design decision with its justification and its impact, and checks the design against its design qualities: availability, manageability, performance, recoverability and security. The design here works the same way. The difference is ownership: the architect writes the decisions, and the customer's input arrives as requirements and constraints.

## Exercise

Take one requirement of your own. Write two realistic designs for it, choose one, and fill in the six fields. Name the constraint that decided it, and what would have to change for the other design to win.
