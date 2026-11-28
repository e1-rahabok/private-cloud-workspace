"""Planted cases for tools/milestone_review.py (R-WS-015, T-WS-015a). Run: python -m unittest discover -s tools -p "test_*.py"."""
import re
import unittest

import milestone_review as review

BRIEF_TEXT = """## Constraints

- **CONSTRAINT-1 The author's review time.** The author cannot review each pull request. Why: one person, with other work. Source: the author, 2026-11-26.

## Risks

- **RISK-1 Copies of a fact drift apart.** Effect: two screens show one KPI differently. Reduced by: a check on every change (R-X-001). Acts: Claude.

## Out of release 1.0

- **SCOPE-9 A second language.** Reason: nobody asked for it yet.
"""

ROADMAP_TEXT = """### M1 First: done

- [x] Done work.
- [x] Approval: the author approves M1.

### M2 Second

- **In plain words:** Two parts hold one fact, and a check compares them.
- **What changes:** Nothing for visitors. For you, one name for one KPI.
- **Left out on purpose:** The lab checks wait for the lab session with you.
- **What I need from you:** confirm the facts marked as your input, and approve the milestone.
- **Risks:** RISK-1 (in the brief).
- [x] A finished piece of work.
- [ ] An open piece of work.
- [ ] Approval: the author approves M2.

### M3 Third

- **The author:** gives the gateway key at the start.
"""


def req(title, why, source, **extra):
    base = {"file": "x.md", "link": "https://example.invalid/x.md", "area": "The workspace", "title": title, "anchor": "a",
            "dropped": False, "why": why, "source": source, "anywhere": 1, "lab": 0, "milestones": set(), "after": False}
    base.update(extra)
    return base


class PlantedPages(unittest.TestCase):
    def setUp(self):
        self.brief = review.brief_items(BRIEF_TEXT)
        self.sections = review.roadmap_sections(ROADMAP_TEXT)
        review.TITLES.clear()
        review.TITLES.update({i: b["title"] for i, b in self.brief.items()})
        self.reqs = {
            "R-X-001": req("Every contract is checked.", "a contract no code checks breaks without notice (CONSTRAINT-1).",
                           'the author, 2026-11-26: "I expect you to check all the contracts"'),
            "R-X-002": req("Checks run on every change.", "a break costs least before merge.", "DESIGN-5."),
            "R-X-003": req("Dropped: an old rule", "", "DESIGN-4.", dropped=True),
        }

    def build(self, mid="M2", state="open", current="M2"):
        ids = ["R-X-001", "R-X-002", "R-X-003"]
        return review.page(mid, self.sections[mid]["title"], ids, self.reqs, self.sections[mid], self.brief, state, current)

    def test_an_answer_of_the_author_lands_under_facts_to_confirm_and_a_design_choice_under_work_built(self):
        text = self.build()
        confirm = text.split("## Facts you confirm")[1].split("## Work I built and own")[0]
        built = text.split("## Work I built and own")[1].split("## Scope left out on purpose")[0]
        self.assertIn("Every contract is checked.", confirm)
        self.assertIn("I expect you to check all the contracts", confirm)
        self.assertNotIn("Checks run on every change.", confirm)
        self.assertIn("Checks run on every change.", built)

    def test_a_brief_item_a_requirement_cites_is_shown_in_words_without_its_id(self):
        text = self.build()
        self.assertIn("The author's review time", text)
        self.assertNotIn("CONSTRAINT-1", text)
        self.assertEqual(review.page_problems("M2", text, self.sections["M2"], "M2"), [])

    def test_the_sections_come_in_the_order_the_requirement_names(self):
        text = self.build()
        self.assertEqual(re.findall(r"^## (.+)$", text, re.M), review.SECTIONS)

    def test_the_risk_of_the_roadmap_field_is_listed_with_what_reduces_it(self):
        text = self.build()
        risks = text.split("## Risks")[1].split("## Testing")[0]
        self.assertIn("Copies of a fact drift apart", risks)
        self.assertIn("Reduced by", risks)

    def test_a_dropped_requirement_is_named_apart(self):
        text = self.build()
        self.assertIn("Dropped from this milestone on purpose", text)
        self.assertIn("An old rule", text)

    def test_unticked_work_says_the_milestone_is_not_finished(self):
        text = self.build()
        self.assertIn("Not ready", text)
        self.assertIn("not finished", text.split("## Testing")[1])

    def test_finished_work_says_every_test_passes_with_no_count(self):
        self.sections["M2"]["open_work"] = []
        text = self.build()
        self.assertIn("Ready for your approval.", text)
        self.assertIn("I ran every test of this milestone, and all of them pass.", text)
        self.assertEqual(review.page_problems("M2", text, self.sections["M2"], "M2"), [])

    def test_a_milestone_that_has_not_opened_says_so_and_claims_no_test(self):
        text = review.page("M3", "Third", [], {}, self.sections["M3"], self.brief, "later", "M2")
        self.assertIn("Not started: this milestone opens after M2", text)
        self.assertIn("nothing has been tested", text.split("## Testing")[1])
        self.assertIn("I write this when the milestone opens.", text)
        self.assertIn("In the plan, the author gives the gateway key at the start.", text)

    def test_a_test_count_an_id_or_a_file_name_makes_the_check_fail(self):
        for planted, what in (("Tests: 2 anywhere, 0 lab.", "a test count"), ("See R-WS-001 for it.", "an ID"),
                              ("Read CLAUDE-PROJECT.md first.", "a file name"), ("It follows DESIGN-7.", "an ID")):
            problems = review.page_problems("M2", self.build() + planted + "\n", self.sections["M2"], "M2")
            self.assertTrue(any(what in p for p in problems), (planted, problems))

    def test_a_missing_field_or_section_of_the_open_milestone_makes_the_check_fail(self):
        del self.sections["M2"]["fields"]["need"]
        problems = review.page_problems("M2", self.build(), self.sections["M2"], "M2")
        self.assertTrue(any("What I need from you" in p for p in problems), problems)
        broken = self.build().replace("## Risks", "## Dangers")
        problems = review.page_problems("M2", broken, self.sections["M2"], "M2")
        self.assertTrue(any("has the sections" in p for p in problems), problems)

    def test_a_file_name_in_copied_text_becomes_words(self):
        self.assertEqual(review.plain("Read [visitor-experience.md](../visitor-experience.md) and KNOWLEDGE-ENGINEERING.md."),
                         "Read visitor experience and knowledge engineering.")

    def test_an_id_in_parentheses_is_dropped_and_a_brief_id_becomes_its_title(self):
        self.assertEqual(review.plain("The rule holds (R-WS-001, DESIGN-4)."), "The rule holds.")
        self.assertEqual(review.plain("It rests on RISK-1."), "It rests on “Copies of a fact drift apart”.")


if __name__ == "__main__":
    unittest.main()
