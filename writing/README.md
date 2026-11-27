# Writing rules

The general writing rules of every repository of Private Cloud Manager, held once, here (R-WS-006 in [workspace.md](../spec/requirements/workspace.md); [WD-023](../DECISIONS.md)). They apply to documents, commit messages and pull request text. Agent E2's knowledge files follow these rules plus the rules particular to them, in agent-e2's [writing.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/writing.md).

## Two kinds of document

- Documents for people: plain prose for a reader on GitHub.
- Documents for machines: CLAUDE.md, CLAUDE-PROJECT.md, requirement files, templates and Agent E2's knowledge files. They are written for an agent or a model to follow: one rule or fact per bullet, the trigger before the action, exact names. A heading may state a claim, as a requirement title states a behaviour.
- Records kept as they were said, such as the interview's answers, are not rewritten.

## Rules for every document

- One fact per bullet or table row, so a mistake sits on one line.
- One paragraph is one source line. GitHub joins wrapped lines into one sentence.
- Plain words and short sentences that state the fact itself: no filler, no praise, no hedging, no summary lines.
- No adjective where a number or a mechanism can stand. Name the thing before saying what it does: verbs such as covers, serves and uses with nothing named read as generated text.
- Full sentences. No slogans, no aphorism in place of the mechanism, no "X, not Y" where a plain statement says it. Judge a line with the lines around it.
- Quotation marks only for verbatim text.
- Every file reference is a link, and every ID is given its meaning or a glossary link on first use.
- The flagged phrases of generated text, each with its plain replacement: [flagged-phrases.yaml](flagged-phrases.yaml).

## Rules for documents for people

- Titles and headings are noun phrases that name the topic, as in a reference book: "Sub-metric formulas" names a topic, where "How each sub-metric is calculated" asks a question.
- No questions, no openers How, Why, What, When, Where, Which or Who, no commands and no claims in a heading. A claim is a fact: it goes in a bullet under the heading.
- At most 8 words in a title and 9 in a heading; words in parentheses do not count.
- Tables have short cells, about 12 words and at most 16, and at most 4 columns when cells hold text; a table of numbers can have more. A row with a long explanation becomes one bullet block: a bold item, one sub-bullet per field.

## The check

- [tools/style.py](../tools/style.py) checks the flagged phrases in every document, and the headings and tables in documents for people. With `--repo` it checks a child repository's clone.
- What no pattern finds, slogans, "X, not Y", hedging and praise, is left to review: read each changed line with the lines around it.
