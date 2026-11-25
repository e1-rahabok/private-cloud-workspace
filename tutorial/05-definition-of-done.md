# 5. Definition of done

## The idea

A goal such as "connect the app to the live system" is a direction, not an instruction. An agent cannot tell when it has finished, so it stops when the work looks finished. Turn each goal into a short list of statements, each of which can be checked.

## Before and after

**Before:** "Connect PCM to live VCF Operations."

**After** (an early draft of ROADMAP, M3):

- The demo control has "Live VCF Operations". Choosing it switches PCM's data to the lab; "Synthetic ACME" switches back. ACME stays the default.
- For one lab cluster, the Performance tab shows Cluster Performance for the last 24 hours, read from the live system. Now, Worst and the 95th percentile match the live system for the same window, within rounding.
- Every part under Details comes from a real metric key. None is synthetic.
- A missing key or a failed read shows as no data or stale, never as zero or green.
- The AI panel's answer names the same worst part the live system shows.
- No secret is in any repository.
- All synthetic-mode tests still pass.

Each line is something a person or a script can check. The list also answers questions the agent would otherwise guess: does synthetic mode stay? (yes); what if a value is missing? (show stale, never green); how close must the numbers be? (within rounding).

## How to write one

- **Start with what a user sees.** "The tab shows X for the last 24 hours" is checkable. "Integrate the API" is not.
- **Name the failure cases.** What happens when data is missing, late, or wrong? The agent will not ask unless told to.
- **Say what must not change.** Existing tests still pass, the default stays the default.
- **Keep it short.** Five to eight lines. A long list hides the important lines.

## Who writes it

The agent drafts it from the goal, the map and the existing decisions. The human reviews and corrects it. Reviewing six lines takes minutes; reviewing the code that results from a misunderstood goal takes hours.

## In this case study

The first draft of that definition said "PCM changes from synthetic data to live data". The author corrected it: both stay, because the lab is too quiet to show the product well. One line in the specification; a large piece of wasted work avoided.

## Exercise

Take one goal from your current backlog. Write it as five checkable statements. Show them to someone who knows the system and ask which line they disagree with.
