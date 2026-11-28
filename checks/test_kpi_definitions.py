"""Planted breaks for check C1 (checks/kpi_definitions.py): each one must make the check fail and name the part.

Reads the clones of agent-e2 and PCM-Adapter next to this repository, as the check does, and changes copies in
memory or in a temporary folder only. Run: python -m unittest discover -s checks -p "test_*.py"
"""
from __future__ import annotations

import copy
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import kpi_definitions as c1

REPOS = Path(__file__).resolve().parents[2]
AGENT_E2, ADAPTER = REPOS / "agent-e2", REPOS / "PCM-Adapter"


@unittest.skipUnless(AGENT_E2.is_dir() and ADAPTER.is_dir(), "needs the clones of agent-e2 and PCM-Adapter")
class PlantedBreaks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        problems: list[str] = []
        cls.catalog = c1.load_catalog(AGENT_E2, problems)
        cls.adapter = c1.load_adapter(ADAPTER)
        cls.load_problems = problems

    def run_compare(self, catalog=None, adapter=None, gaps=None):
        known: list[str] = []
        problems = c1.compare(catalog or self.catalog, adapter or self.adapter, known, gaps)
        return problems, known

    def test_main_branches_agree(self):
        problems, _ = self.run_compare()
        self.assertEqual(self.load_problems + problems, [])

    def test_a_changed_limit_fails_and_names_the_part(self):
        catalog = copy.deepcopy(self.catalog)
        row = catalog["Cluster Risk"]["Worst ESXi CPU Imbalance"]
        interval = next(k for k in ("5m", "20s", "2s") if row.get(k))
        row[interval] = row[interval][:4] + [row[interval][4] + 1]
        problems, _ = self.run_compare(catalog=catalog)
        self.assertTrue(any("Worst ESXi CPU imbalance" in p and "limits" in p for p in problems), problems)

    def test_a_key_the_adapter_lacks_fails(self):
        adapter = copy.deepcopy(self.adapter)
        del adapter["ESXi Performance"]["Worst VM CPU Ready"]
        problems, _ = self.run_compare(adapter=adapter)
        self.assertTrue(any("'Worst VM CPU Ready'" in p and "not in the adapter" in p for p in problems), problems)

    def test_a_new_name_gap_fails(self):
        adapter = copy.deepcopy(self.adapter)
        metric, _ = adapter["Cluster Risk"]["Worst ESXi CPU Imbalance"]
        adapter["Cluster Risk"]["Worst ESXi CPU Imbalance"] = (metric, "CPU imbalance, renamed")
        problems, _ = self.run_compare(adapter=adapter)
        self.assertTrue(any("CPU imbalance, renamed" in p for p in problems), problems)

    def test_a_stale_baseline_entry_fails(self):
        gaps = copy.deepcopy(c1.NAME_GAPS)
        gaps.setdefault("Cluster Risk", set()).add("Worst ESXi CPU Imbalance")
        problems, _ = self.run_compare(gaps=gaps)
        self.assertTrue(any("NAME_GAPS lists 'Worst ESXi CPU Imbalance'" in p for p in problems), problems)

    def test_a_row_without_key_and_a_key_used_twice_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(AGENT_E2 / "knowledge" / "catalog", Path(tmp) / "knowledge" / "catalog")
            risk = Path(tmp) / "knowledge" / "catalog" / "thresholds-risk.yaml"
            text = risk.read_text(encoding="utf-8")
            keys = re.findall(r', key: ("[^"]*")', text)
            text = text.replace(f", key: {keys[0]}", "", 1).replace(f", key: {keys[2]}", f", key: {keys[1]}", 1)
            risk.write_text(text, encoding="utf-8")
            problems: list[str] = []
            c1.load_catalog(Path(tmp), problems)
        self.assertTrue(any("has no key" in p for p in problems), problems)
        self.assertTrue(any("twice" in p for p in problems), problems)

    def test_an_interval_that_differs_fails(self):
        adapter = copy.deepcopy(self.adapter)
        metric, label = adapter["VM Performance"]["CPU Ready"]
        adapter["VM Performance"]["CPU Ready"] = (metric._replace(interval="5m"), label)
        problems, _ = self.run_compare(adapter=adapter)
        self.assertTrue(any("interval" in p and "CPU Ready" in p for p in problems), problems)

    def periodic_problems(self, edit):
        """compare_periodic on a copy of the catalog changed by edit(folder)."""
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(AGENT_E2 / "knowledge" / "catalog", Path(tmp) / "knowledge" / "catalog")
            edit(Path(tmp) / "knowledge" / "catalog")
            return c1.compare_periodic(Path(tmp), [])

    def test_the_periodic_check_agrees_on_main(self):
        self.assertEqual(c1.compare_periodic(AGENT_E2, []), [])

    def test_a_changed_score_row_fails(self):
        def edit(folder):
            f = folder / "thresholds-risk.yaml"
            f.write_text(f.read_text(encoding="utf-8").replace("5m: [0, 25, 50, 75, 100]", "5m: [0, 30, 50, 75, 100]", 1),
                         encoding="utf-8")
        problems = self.periodic_problems(edit)
        self.assertTrue(any("Cluster Risk score bands" in p for p in problems), problems)

    def test_a_kpi_without_a_score_row_fails(self):
        def edit(folder):
            f = folder / "thresholds-performance.yaml"
            text = f.read_text(encoding="utf-8")
            f.write_text(text[:text.index("\nscore:\n")] + "\n", encoding="utf-8")
        problems = self.periodic_problems(edit)
        self.assertTrue(any("Cluster Performance, which has no score row" in p for p in problems), problems)

    def test_a_changed_closure_level_fails(self):
        def edit(folder):
            f = folder / "thresholds-capacity.yaml"
            text = f.read_text(encoding="utf-8")
            at = text.index("id: closure-cluster-consumption-red")
            end = text.index("value: 80", at)
            f.write_text(text[:end] + "value: 85" + text[end + len("value: 80"):], encoding="utf-8")
        problems = self.periodic_problems(edit)
        self.assertTrue(any("Consumption red" in p for p in problems), problems)

    def test_a_changed_excluded_when_green_fails(self):
        adapter = copy.deepcopy(self.adapter)
        metric, label = adapter["Cluster Risk"]["Worst ESXi CPU Imbalance"]
        adapter["Cluster Risk"]["Worst ESXi CPU Imbalance"] = (metric._replace(skip_when_green=not metric.skip_when_green), label)
        problems, _ = self.run_compare(adapter=adapter)
        self.assertTrue(any("excluded when green" in p and "CPU imbalance" in p for p in problems), problems)

    def test_a_changed_closure_window_fails(self):
        def edit(folder):
            f = folder / "thresholds-capacity.yaml"
            text = f.read_text(encoding="utf-8")
            at = text.index("id: closure-cluster-performance-red")
            start = text.rindex("- ", 0, at)
            part = text[start:at + 200].replace("5th percentile of the last 24 hours", "10th percentile of the last 24 hours", 1)
            f.write_text(text[:start] + part + text[at + 200:], encoding="utf-8")
        problems = self.periodic_problems(edit)
        self.assertTrue(any("closure-cluster-performance-red" in p and "percentile" in p for p in problems), problems)


if __name__ == "__main__":
    unittest.main()
