# 10. Trust in AI-written content

## The problem

This project publishes expert knowledge on a public website, and an AI writes the pages from a knowledge base. For an expert site, being trusted is everything, and one confident error under the author's name costs more than many good pages earn.

This is not a new problem. Publishers, documentation teams and encyclopedias have always had more to publish than they could check. What AI changes is the balance: writing becomes almost free, so checking becomes the bottleneck. The question is where to spend a small amount of checking so that it counts.

## Two different risks

They need different fixes, so it helps to separate them.

1. **The source is wrong.** A fact in the knowledge base is false. Books written by hand carry this risk too.
2. **The derivation is wrong.** A correct fact is changed on its way into an article, a quiz question or a summary: something added, dropped or bent. AI adds this risk, and it grows with every new form the same knowledge is published in.

## What works without AI

The established practices still apply:

- review by named experts before publishing;
- the date and source of each page, and when it was last checked;
- citations to primary sources, such as vendor documentation, so readers can verify;
- a public corrections policy, with errors fixed in the open;
- a way for readers to report a problem on any page;
- honest labels such as "draft" or "last reviewed on";
- publishing less, and better.

None of these scales to hundreds of pages with one reviewer who has no time, which was this project's situation.

## What AI adds

AI cannot replace an expert's judgement, but it can reduce how much of that judgement each page needs.

- **Rule on disagreements instead of reviewing everything.** An AI sweep reads the whole knowledge base and lists only the doubtful places: two files with different numbers for the same thing, a claim that contradicts current vendor documentation, a statement with no support. The expert then rules on perhaps forty flags, not three hundred files. A second, independent model checks the first one's flags, to cut false alarms.
- **Let scripts check what scripts can check.** Numbers, limits and formulas live in one catalog, and every page, quiz and calculator is checked against it automatically.
- **Test every rewrite.** Extract the claims from a generated page and compare them with the source file. Anything added or missing fails the page.
- **Review in order of exposure.** Start with the pages people actually read, and the files the AI assistant cites most. A small number of pages usually carries most of the risk.
- **Prepare the reviewer's work.** For a human reviewer, AI gathers the claims, their sources and the open flags into a short packet, so a review takes minutes.
- **Use the readers.** A "report a problem" link on every section, AI sorting the reports and drafting fixes, and the expert approving them. Readers become the largest review team.

## Calculators are not automatically safe

It is tempting to think that a calculator, with no AI in it, is the most accurate part of a site. It is the easiest part to make trustworthy, but only if three things hold: its formula matches the current knowledge, its code matches the formula, and it is used for the question it was built for. In this project a calculator ported from an old spreadsheet still used an overcommit ratio of 4 to 1 where the current knowledge says 3 to 1. It was precise, and wrong. The fix is to take its numbers from the catalog and to keep worked examples that every build must reproduce.

## Community

The strongest answer to the review bottleneck is other experts. A community of practitioners who can report errors, suggest corrections with evidence, and review an area they know, turns one tired reviewer into many. Two rules make it work: contributors are identified (anonymous reading is fine, anonymous editing is not), and every correction carries evidence, such as a vendor document, a measurement or a screenshot. The original author stays the editor who rules on disputes.

## Exercise

Pick ten pages of something you publish. For each, which of the two risks applies, and which of the measures above would catch an error in it?
