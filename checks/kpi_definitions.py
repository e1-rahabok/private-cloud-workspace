# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Check C1: the KPI definitions in PCM-Adapter match the Agent E2 catalog.

Agent E2 owns every KPI definition (CONTRACTS.md, C1). PCM-Adapter implements them.
For each KPI this check compares, sub-metric by sub-metric:
  - the sub-metric exists on both sides, matched by key: the catalog row's `key` against the
    name the adapter's KPI module gives the row (R-KPI-001),
  - its name: the adapter's label (its LABELS table, else the row name) against the catalog's
    metric name without its unit in brackets (R-KPI-003),
  - the five limits [best, green, yellow, orange, zero-at] (R-KPI-002),
  - "excluded when green" (the adapter's skip_when_green),
  - the interval: the adapter row's interval against the catalog interval whose limits matched (R-ADP-008).
It also compares the band table of the adapter's Periodic Cluster Check with the catalog's score row of each KPI it
colours (R-KPI-005), and its closure levels and window with the catalog's Close for Business decisions (R-KPI-006).
Each catalog row must have a key and five limits for at least one interval, and no KPI may use
one key twice. A ratio has no unit, so a unit is not required.

Known name gaps (NAME_GAPS below) are a baseline: they are reported as KNOWN and do not fail.
A new gap fails. A baseline entry that no longer applies also fails, so the baseline only shrinks.
checks/test_kpi_definitions.py plants a break of each kind and expects this check to fail on it.

It reads both repositories from local clones and connects to nothing.
Exit 0: no new difference. Exit 1: a difference. Exit 2: a repository could not be read.
"""
from __future__ import annotations

import argparse
import importlib
import re
import sys
import types
from pathlib import Path

import yaml

# Catalog files and sections that hold KPI sub-metrics, in the Agent E2 repository.
CATALOG_SECTIONS = [
    ("knowledge/catalog/thresholds-performance.yaml", "kpi"),
    ("knowledge/catalog/thresholds-risk.yaml", "model"),
    ("knowledge/catalog/thresholds-capacity.yaml", "model"),
]

# The KPI a catalog row belongs to, from the last part of its kb path.
KPI_BY_KB = {
    "cluster-performance": "Cluster Performance",
    "esxi-performance": "ESXi Performance",
    "vm-performance": "VM Performance",
    "guest-os-performance": "Guest OS Performance",
    "cluster-risk": "Cluster Risk",
    "cluster-consumption": "Cluster Consumption",
}

# The adapter module that implements each KPI, under "Management Pack/app".
ADAPTER_MODULES = {
    "Cluster Performance": "metrics.cluster.cluster_performance_metrics",
    "ESXi Performance": "metrics.host.esxi_performance_metrics",
    "VM Performance": "metrics.vm.vm_performance_metrics",
    "Guest OS Performance": "metrics.vm.guest_os_performance_metrics",
    "Cluster Risk": "metrics.cluster.cluster_risk_metrics",
    "Cluster Consumption": "metrics.cluster.cluster_consumption_metrics",
}

# Known name gaps (Q-WS-1): the keys of rows whose adapter label differs from the catalog name. Empty since R-ADP-006;
# a new gap fails. An entry may be added only with a question in OPEN-QUESTIONS.md, and the check fails once it is fixed.
NAME_GAPS: dict[str, set[str]] = {}

# Close for Business decisions compared with the adapter's levels: decision id -> (KPI, band). Cluster Risk is a known
# gap until Q-WS-138 is answered: the catalog keeps a production and a non-production level, the adapter one level.
CLOSURE_DECISIONS = {
    "closure-cluster-consumption-red": ("Consumption", "red"),
    "closure-cluster-consumption-orange": ("Consumption", "orange"),
    "closure-cluster-performance-red": ("Performance", "red"),
    "closure-cluster-performance-orange": ("Performance", "orange"),
}
CLOSURE_GAPS = {"closure-cluster-risk-prod": "Q-WS-138", "closure-cluster-risk-nonprod": "Q-WS-138"}

# The score row of each KPI the Periodic Cluster Check colours, by the last part of its kb path.
SCORE_ROWS = {"Performance": "cluster-performance", "Risk": "cluster-risk", "Consumption": "cluster-consumption"}
SCORE_FILES = ["knowledge/catalog/thresholds-performance.yaml", "knowledge/catalog/thresholds-risk.yaml",
               "knowledge/catalog/thresholds-capacity.yaml"]
PERCENTILE = re.compile(r"(\d+)(?:st|nd|rd|th) percentile of the last (\d+) hours")

UNIT_SUFFIX = re.compile(r"\s*\([^()]*\)\s*$")


def norm(name: str) -> str:
    """Compare names without case, extra spaces or a trailing unit in brackets."""
    return " ".join(UNIT_SUFFIX.sub("", name).lower().split())


def load_catalog(agent_e2: Path, problems: list[str]) -> dict[str, dict[str, dict]]:
    """{KPI: {key: row}} from the Agent E2 catalog. A row without a key or limits, or a key used twice, is a problem."""
    kpis: dict[str, dict[str, dict]] = {}
    for rel, section in CATALOG_SECTIONS:
        data = yaml.safe_load((agent_e2 / rel).read_text(encoding="utf-8"))
        for row in data.get(section) or []:
            kpi = KPI_BY_KB.get(str(row.get("kb", "")).rsplit("/", 1)[-1])
            if kpi is None:
                continue
            name = row.get("metric", "?")
            if not row.get("key"):
                problems.append(f"{kpi}: catalog row '{name}' has no key")
                continue
            if not any(isinstance(row.get(k), list) and len(row[k]) == 5 for k in ("5m", "20s", "2s")):
                problems.append(f"{kpi}: catalog row '{name}' has no five limits for any interval")
            if row["key"] in kpis.get(kpi, {}):
                problems.append(f"{kpi}: the catalog uses key '{row['key']}' twice")
            kpis.setdefault(kpi, {})[row["key"]] = row
    return kpis


def stub_sdk() -> None:
    """The adapter imports the VCF Operations SDK; this check needs only its tables."""
    for name in ("aria", "aria.ops", "aria.ops.object", "aria.ops.suite_api_client"):
        sys.modules.setdefault(name, types.ModuleType(name))
    sys.modules["aria.ops.object"].Object = type("Object", (), {})
    sys.modules["aria.ops.suite_api_client"].SuiteApiClient = type("SuiteApiClient", (), {})


def load_adapter(adapter: Path) -> dict[str, dict[str, tuple[object, str]]]:
    """{KPI: {row name: (Metric, label)}} from the adapter's KPI modules."""
    sys.path.insert(0, str(adapter / "Management Pack" / "app"))
    stub_sdk()
    kpis: dict[str, dict[str, tuple[object, str]]] = {}
    for kpi, module_name in ADAPTER_MODULES.items():
        module = importlib.import_module(module_name)
        labels = getattr(module, "LABELS", {})
        kpis[kpi] = {m.name: (m, labels.get(m.name, m.name)) for m in module.METRICS}
    return kpis


def limits_of(metric) -> list[float]:
    return [metric.best, metric.green, metric.yellow, metric.orange, metric.zero_at]


def compare(catalog: dict, adapter: dict, known: list[str], gaps: dict | None = None) -> list[str]:
    """The differences between the catalog and the adapter, by key. Known name gaps go to known."""
    gaps = NAME_GAPS if gaps is None else gaps
    problems: list[str] = []
    for kpi in ADAPTER_MODULES:
        cat_rows, ada_rows = catalog.get(kpi, {}), adapter.get(kpi, {})
        for key in sorted(cat_rows.keys() - ada_rows.keys()):
            problems.append(f"{kpi}: key '{key}' ('{cat_rows[key]['metric']}') is in the Agent E2 catalog but not in the adapter")
        for key in sorted(ada_rows.keys() - cat_rows.keys()):
            problems.append(f"{kpi}: key '{key}' is in the adapter but not in the Agent E2 catalog")
        for key in sorted(set(gaps.get(kpi, set())) - ada_rows.keys()):
            problems.append(f"{kpi}: NAME_GAPS lists '{key}', which the adapter no longer has: delete the entry")
        for key in sorted(cat_rows.keys() & ada_rows.keys()):
            row, (metric, label) = cat_rows[key], ada_rows[key]
            same_name = norm(label) == norm(row["metric"])
            if key in gaps.get(kpi, set()):
                if same_name:
                    problems.append(f"{kpi}: NAME_GAPS lists '{key}', whose label now equals the catalog name: delete the entry")
                else:
                    known.append(f"{kpi}: '{key}' is labelled '{label}', the catalog names it '{row['metric']}'")
            elif not same_name:
                problems.append(f"{kpi}: '{key}' is labelled '{label}', the catalog names it '{row['metric']}'")
            wanted = {k: row[k] for k in ("5m", "20s", "2s") if row.get(k)}
            have = limits_of(metric)
            matched = [k for k, w in wanted.items() if [float(v) for v in w] == [float(v) for v in have]]
            if not matched:
                problems.append(f"{kpi}: '{row['metric']}' limits: catalog {list(wanted.values()) or 'none entered'}, adapter {have}")
            elif getattr(metric, "interval", "") not in matched:
                problems.append(f"{kpi}: '{row['metric']}' interval: catalog {' or '.join(matched)}, "
                                f"adapter {getattr(metric, 'interval', '') or 'none'}")
            if bool(row.get("excluded_when_green", False)) != bool(metric.skip_when_green):
                problems.append(f"{kpi}: '{row['metric']}' excluded when green: catalog "
                                f"{bool(row.get('excluded_when_green', False))}, adapter {bool(metric.skip_when_green)}")
    return problems


def health_limits(row: dict) -> list[float]:
    """A score row's green, yellow and orange limits on the health scale: 100 minus the value when higher is worse."""
    limits = [float(v) for v in row["5m"][1:4]]
    return [100.0 - v for v in limits] if row["direction"] == "above" else limits


def compare_periodic(agent_e2: Path, known: list[str]) -> list[str]:
    """The Periodic Cluster Check's band table, closure levels and window against the catalog (R-KPI-005, R-KPI-006)."""
    pcc = importlib.import_module("metrics.cluster.periodic_cluster_check")
    problems: list[str] = []
    scores = {}
    for rel in SCORE_FILES:
        for row in yaml.safe_load((agent_e2 / rel).read_text(encoding="utf-8")).get("score") or []:
            scores[str(row.get("kb", "")).rsplit("/", 1)[-1]] = row
    bands = [pcc.YELLOW_BELOW, pcc.ORANGE_BELOW, pcc.RED_BELOW]
    for kpi, kb in SCORE_ROWS.items():
        row = scores.get(kb)
        if row is None or not row.get("5m"):
            problems.append(f"Periodic Cluster Check colours Cluster {kpi}, which has no score row in the catalog")
        elif health_limits(row) != [float(b) for b in bands]:
            problems.append(f"Cluster {kpi} score bands: catalog {row['5m']} ({row['direction']}), "
                            f"adapter yellow/orange/red below {bands} on the health scale")
    decisions = {d["id"]: d for d in yaml.safe_load(
        (agent_e2 / "knowledge/catalog/thresholds-capacity.yaml").read_text(encoding="utf-8")).get("decisions") or []}
    levels = {"red": pcc.CLOSE_RED_BELOW, "orange": pcc.CLOSE_ORANGE_BELOW}
    for did, (kpi, band) in CLOSURE_DECISIONS.items():
        d = decisions.get(did)
        if d is None:
            problems.append(f"Close for Business: the catalog has no decision '{did}'")
            continue
        value = float(d["value"])
        health = 100.0 - value if d["operator"] == ">" else value
        if health != float(levels[band]):
            problems.append(f"Close for Business, {kpi} {band}: catalog {d['operator']} {d['value']}, "
                            f"adapter {band} below {levels[band]} on the health scale")
        m = PERCENTILE.search(d["metric"])
        if not m:
            problems.append(f"Close for Business, '{did}': no percentile and window in '{d['metric']}'")
            continue
        percentile, hours = int(m.group(1)), int(m.group(2))
        worst = percentile if kpi == "Performance" else 100 - percentile
        if (worst, hours) != (pcc.DEFAULT_WORST_PERCENT, int(pcc.DEFAULT_PERIOD)):
            problems.append(f"Close for Business, '{did}': catalog {percentile}th percentile of {hours} hours, adapter "
                            f"{pcc.DEFAULT_WORST_PERCENT} % of the worst samples ignored over {pcc.DEFAULT_PERIOD} hours")
    for did, question in CLOSURE_GAPS.items():
        if did in decisions:
            known.append(f"Close for Business: '{did}' is not compared until {question} is answered")
        else:
            problems.append(f"CLOSURE_GAPS lists '{did}', which the catalog no longer has: delete the entry")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repos", type=Path, default=Path(__file__).resolve().parents[2],
                        help="folder that holds the clones agent-e2 and PCM-Adapter (default: next to this repository)")
    args = parser.parse_args()
    agent_e2, adapter = args.repos / "agent-e2", args.repos / "PCM-Adapter"
    for repo in (agent_e2, adapter):
        if not repo.is_dir():
            print(f"ERROR: {repo} not found. Clone it, or pass --repos.")
            return 2
    problems: list[str] = []
    catalog, implemented = load_catalog(agent_e2, problems), load_adapter(adapter)
    known: list[str] = []
    problems += compare(catalog, implemented, known)
    problems += compare_periodic(agent_e2, known)
    checked = sum(len(v) for v in catalog.values())
    for k in known:
        print(f"KNOWN {k}")
    for p in problems:
        print(f"FAIL {p}")
    print(f"C1 KPI definitions: {checked} catalog sub-metrics in {len(ADAPTER_MODULES)} KPIs, "
          f"{len(problems)} difference(s), {len(known)} known gap(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
