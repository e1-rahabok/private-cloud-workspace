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
  - "excluded when green" (the adapter's skip_when_green).
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

# Known name gaps (Q-WS-1; R-ADP-006 closes them in M2): the keys of the rows whose adapter label differs
# from the catalog name. Close a gap by giving the adapter row the catalog name (its LABELS table), then
# delete the key here; the check fails until you do.
NAME_GAPS = {
    "VM Performance": {"CPU Co-Stop", "CPU Ready", "CPU Overlap", "Disk Latency", "Network Dropped Tx", "CPU Run",
                       "Memory Ballooned"},
    "Guest OS Performance": {"Guest CPU Run Queue per vCPU", "Guest Disk Queue", "Guest Free Memory",
                             "Guest Page-Out Rate"},
}

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
            wanted = [row[k] for k in ("5m", "20s", "2s") if row.get(k)]
            have = limits_of(metric)
            if not any([float(v) for v in w] == [float(v) for v in have] for w in wanted):
                problems.append(f"{kpi}: '{row['metric']}' limits: catalog {wanted or 'none entered'}, adapter {have}")
            if bool(row.get("excluded_when_green", False)) != bool(metric.skip_when_green):
                problems.append(f"{kpi}: '{row['metric']}' excluded when green: catalog "
                                f"{bool(row.get('excluded_when_green', False))}, adapter {bool(metric.skip_when_green)}")
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
    checked = sum(len(v) for v in catalog.values())
    for k in known:
        print(f"KNOWN {k}")
    for p in problems:
        print(f"FAIL {p}")
    print(f"C1 KPI definitions: {checked} catalog sub-metrics in {len(ADAPTER_MODULES)} KPIs, "
          f"{len(problems)} difference(s), {len(known)} known name gap(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
