# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Check C1: the KPI definitions in PCM-Adapter match the Agent E2 catalog.

Agent E2 owns every KPI definition (CONTRACTS.md, C1). PCM-Adapter implements them.
For each KPI this check compares, sub-metric by sub-metric:
  - the sub-metric exists on both sides (matched by name: the adapter's label against
    the catalog's metric name without its unit in brackets),
  - the five limits [best, green, yellow, orange, zero-at],
  - "excluded when green" (the adapter's skip_when_green).

Known name gaps (NAME_GAPS below) are a baseline: they are reported as KNOWN and do not fail,
but their limits are still compared. A new gap fails. A baseline entry that no longer applies
also fails, so the baseline only shrinks.

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

# Known name gaps (OPEN-QUESTIONS.md, Q-WS-1): adapter name -> catalog name, for the rows the adapter
# publishes under a name other than the catalog's. Close a gap by giving the adapter row the catalog
# name (its LABELS table), then delete the line here; the check fails until you do.
NAME_GAPS = {
    "VM Performance": {
        "CPU Co-Stop": "Peak CPU Co-stop among any vCPU",
        "CPU Ready": "Peak CPU Ready among any vCPU",
        "CPU Overlap": "Peak CPU Overlap",
        "Disk Latency": "Peak read/write latency among vDisks",
        "Network Dropped Tx": "Peak network TX dropped packets",
        "CPU Run": "CPU Net Run",
        "Memory Ballooned": "VM Memory Ballooned",
    },
    "Guest OS Performance": {
        "Guest CPU Run Queue per vCPU": "Peak vCPU run queue length",
        "Guest Disk Queue": "Peak disk queue length",
        "Guest Free Memory": "Free memory",
        "Guest Page-Out Rate": "Memory page-out rate",
    },
}

UNIT_SUFFIX = re.compile(r"\s*\([^()]*\)\s*$")


def norm(name: str) -> str:
    """Compare names without case, extra spaces or a trailing unit in brackets."""
    return " ".join(UNIT_SUFFIX.sub("", name).lower().split())


def load_catalog(agent_e2: Path) -> dict[str, dict[str, dict]]:
    """{KPI: {normalized name: row}} from the Agent E2 catalog."""
    kpis: dict[str, dict[str, dict]] = {}
    for rel, section in CATALOG_SECTIONS:
        data = yaml.safe_load((agent_e2 / rel).read_text(encoding="utf-8"))
        for row in data.get(section) or []:
            kpi = KPI_BY_KB.get(str(row.get("kb", "")).rsplit("/", 1)[-1])
            if kpi is None:
                continue
            kpis.setdefault(kpi, {})[norm(row["metric"])] = row
    return kpis


def stub_sdk() -> None:
    """The adapter imports the VCF Operations SDK; this check needs only its tables."""
    for name in ("aria", "aria.ops", "aria.ops.object", "aria.ops.suite_api_client"):
        sys.modules.setdefault(name, types.ModuleType(name))
    sys.modules["aria.ops.object"].Object = type("Object", (), {})
    sys.modules["aria.ops.suite_api_client"].SuiteApiClient = type("SuiteApiClient", (), {})


def load_adapter(adapter: Path) -> dict[str, dict[str, object]]:
    """{KPI: {normalized label: Metric}} from the adapter's KPI modules."""
    sys.path.insert(0, str(adapter / "Management Pack" / "app"))
    stub_sdk()
    kpis: dict[str, dict[str, object]] = {}
    for kpi, module_name in ADAPTER_MODULES.items():
        module = importlib.import_module(module_name)
        labels = getattr(module, "LABELS", {})
        kpis[kpi] = {norm(labels.get(m.name, m.name)): m for m in module.METRICS}
    return kpis


def resolve_name_gaps(adapter: dict, problems: list[str], known: list[str]) -> None:
    """File each known gap's row under the catalog name, so its limits are compared; a stale entry is a problem."""
    for kpi, gaps in NAME_GAPS.items():
        rows = adapter.get(kpi, {})
        for adapter_name, catalog_name in gaps.items():
            if norm(adapter_name) in rows:
                rows[norm(catalog_name)] = rows.pop(norm(adapter_name))
                known.append(f"{kpi}: adapter names it '{adapter_name}', the catalog '{catalog_name}'")
            else:
                problems.append(f"{kpi}: NAME_GAPS lists '{adapter_name}', which the adapter no longer has: delete the entry")


def limits_of(metric) -> list[float]:
    return [metric.best, metric.green, metric.yellow, metric.orange, metric.zero_at]


def compare(catalog: dict, adapter: dict, known: list[str]) -> list[str]:
    problems: list[str] = []
    resolve_name_gaps(adapter, problems, known)
    for kpi in ADAPTER_MODULES:
        cat_rows, ada_rows = catalog.get(kpi, {}), adapter.get(kpi, {})
        for name in sorted(cat_rows.keys() - ada_rows.keys()):
            problems.append(f"{kpi}: '{cat_rows[name]['metric']}' is in the Agent E2 catalog but not in the adapter")
        for name in sorted(ada_rows.keys() - cat_rows.keys()):
            problems.append(f"{kpi}: '{ada_rows[name].name}' is in the adapter but not in the Agent E2 catalog")
        for name in sorted(cat_rows.keys() & ada_rows.keys()):
            row, metric = cat_rows[name], ada_rows[name]
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
    catalog, implemented = load_catalog(agent_e2), load_adapter(adapter)
    known: list[str] = []
    problems = compare(catalog, implemented, known)
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
