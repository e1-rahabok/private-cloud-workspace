# Roadmap

Stage 1 (SYSTEM.md). Each milestone is a thin slice across the repositories, with a definition of done made of statements that can be checked. A session works on one milestone, stops when the specification does not decide something, and writes the question to [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).

Progress is marked on each line: `[ ]` open, `[x]` done (with the pull request).

## M0 Workspace specification and checks

- [x] SYSTEM, CONTRACTS, DECISIONS, ROADMAP, OPEN-QUESTIONS and CLAUDE.md merged in this repository (#1).
- [x] C1 and C3 run in GitHub Actions on push, pull request, daily and on demand, and pass (#1).
- [ ] A tutorial that teaches the method to others, with this workspace as the case study (`tutorial/`).

## M1 Close the known gaps

- [ ] C1 runs with an empty `NAME_GAPS`: every VM Performance and Guest OS Performance row in PCM-Adapter carries its catalog name (Q-1).
- [ ] C1 also checks the part names PCM uses, from a structured list in PCM's specification instead of prose.
- [ ] No file outside an archive names the old repository VCF-vCommunity-Adapter, in any of the four repositories.
- [ ] Each child repository runs `checks/run_all.py` on its own pull requests, so a break is caught before merge instead of the next day.

## M2 Live VCF Operations in PCM: one cluster, one KPI

Done when:

- [ ] The demo control has "Live VCF Operations". Choosing it switches PCM's data to https://10.115.1.81; "Synthetic ACME" switches back. ACME stays the default.
- [ ] For one lab cluster, the L2 Performance tab shows Cluster Performance for the last 24 hours, read from VCF Operations. Now, Worst and the 95th percentile match VCF Operations for the same window, within rounding.
- [ ] Every part under Details comes from a `vCommunity|` key of that cluster. None is synthetic.
- [ ] A missing key or a failed read shows as no data or stale, never as zero or green (PCM D-041).
- [ ] The Agent E2 panel's answer names the same worst part VCF Operations shows.
- [ ] PCM lists every key it reads in one structured file, and C2 checks each against PCM-Adapter.
- [ ] The credential is in `/etc/pcm/pcm.env` on the lab VM; no secret is in any repository.
- [ ] All synthetic-mode tests still pass.

## M3 Live VCF Operations: the rest of release 1.0

- [ ] The other KPIs and objects on the release 1.0 pages read live data, by the same pattern as M2.
- [ ] C2 also runs against the lab: each listed key has data on at least one object.

## M4 isvara.io content from Agent E2: one pilot page

- [ ] One concept page on isvara.io is generated from the Agent E2 knowledge base, with no hand edits, and reads well for a person.
- [ ] The export from Agent E2 is a written contract (C4) with a check.
- [ ] The author decides from the pilot whether to rebuild the guide, the tools and the assessment the same way.

## M5 Agent E2 on isvara.io

- [ ] Q-4 is decided: where the public Agent E2 runs.
- [ ] isvara.io's chat calls Agent E2 through the C3 contract. AskIO is removed.
- [ ] isvara.io's eval and injection batteries pass against Agent E2.

## M6 isvara.io exam

- [ ] 10 questions for people, short and very hard, each testing understanding of a mechanism, with the reasoning shown after the answer (W-006).
- [ ] The author has reviewed every question and answer.
- [ ] The exam sits next to the 2am game.
