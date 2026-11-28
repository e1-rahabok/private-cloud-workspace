# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "requests"]
# ///
"""Check C3: PCM's Agent E2 client and the Agent E2 service still agree.

Agent E2 owns the API (contract C3 in spec/design/system.md); PCM is its caller. The check starts the real Agent E2
service from its clone in mock mode (no model, no network), then calls it with PCM's own client
code, pcm/core/agent_e2.py, for each endpoint PCM uses. PCM's client turns any error into
source "unavailable" so the panel can say so; that same behaviour would hide a broken contract,
so this check also reads the raw responses and checks every field PCM reads.

Exit 0: the contract holds. Exit 1: a difference. Exit 2: a repository could not be read or the
service did not start.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# What PCM reads from each response, and the type each field must have. None allowed where PCM handles it.
ANSWER_FIELDS = {"type": (str,), "content": (str,), "lead": (str,), "questions": (list,), "files_read": (list,),
                 "computed": (list,), "topic": (dict, type(None)), "model": (str,), "knowledge_commit": (str, type(None))}
TOPIC_FIELDS = {"continues": (bool,), "by": (str,)}
SUGGEST_FIELDS = {"questions": (list,), "situation": (dict, type(None))}

PAGE_FACTS = {"object": {"kind": "cluster", "name": "SG-S-01"}, "pillar": "Performance", "window": "24h",
              "kpis": [{"label": "Cluster Performance", "better": "higher",
                        "points": [[f"2026-10-19T{h:02d}:00:00+08:00", v] for h, v in
                                   zip(range(0, 24), [88, 87, 88, 86, 85, 84, 80, 75, 62, 48, 44, 42] * 2)]}]}


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_service(agent_e2: Path, port: int) -> subprocess.Popen:
    proc = subprocess.Popen([sys.executable, str(agent_e2 / "harness" / "answer_service.py"), "--mock", "--port", str(port)],
                            cwd=agent_e2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    deadline = time.time() + 120
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError("Agent E2 service exited:\n" + (proc.stdout.read() if proc.stdout else ""))
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/v1/health", timeout=2) as r:
                if json.loads(r.read()).get("ok"):
                    return proc
        except OSError:
            time.sleep(1)
    proc.kill()
    raise RuntimeError("Agent E2 service did not answer /v1/health within 120 seconds")


def load_pcm_client(pcm: Path):
    path = pcm / "pcm" / "core" / "agent_e2.py"
    spec = importlib.util.spec_from_file_location("pcm_agent_e2_client", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_fields(name: str, out: dict, fields: dict, problems: list[str]) -> None:
    for field, types in fields.items():
        if field not in out:
            problems.append(f"{name}: response has no '{field}', which PCM reads")
        elif not isinstance(out[field], types):
            problems.append(f"{name}: '{field}' is {type(out[field]).__name__}, PCM expects "
                            + " or ".join(t.__name__ for t in types))


def run(url: str, client) -> list[str]:
    problems: list[str] = []
    history = [{"question": "Which part pulled Cluster Performance down?", "answer": "Highest ESXi network packets."}]

    # /v1/answer: raw response first, then through PCM's client.
    raw = client._post_raw(url + "/v1/answer", {"question": "Why is Cluster Performance low on SG-S-01?",
                                               "facts": PAGE_FACTS, "role": "l2"}, 180)
    check_fields("/v1/answer", raw, ANSWER_FIELDS, problems)
    if raw.get("type") not in ("answer", "clarify"):
        problems.append(f"/v1/answer: type is {raw.get('type')!r}, PCM expects 'answer' or 'clarify'")
    out = client.ask_service(url, "Why is Cluster Performance low on SG-S-01?", PAGE_FACTS, "l2",
                             history=history, topic_choice="continue")
    if out["source"] != "service":
        problems.append(f"/v1/answer through PCM's client: source {out['source']!r}, expected 'service'")

    # /v1/topic
    raw = client._post_raw(url + "/v1/topic", {"question": "And on the host?", "history": history, "topic_choice": "auto"}, 20)
    check_fields("/v1/topic", raw, TOPIC_FIELDS, problems)
    if client.topic_service(url, "And on the host?", history)["source"] != "service":
        problems.append("/v1/topic through PCM's client: not answered by the service")

    # /v1/suggest, page
    raw = client._post_raw(url + "/v1/suggest", {"facts": PAGE_FACTS}, 20)
    check_fields("/v1/suggest (page)", raw, SUGGEST_FIELDS, problems)
    if len(raw.get("questions") or []) > 3:
        problems.append("/v1/suggest (page): more than 3 questions; PCM shows 3")
    if client.suggest_service(url, PAGE_FACTS, 20)["source"] != "service":
        problems.append("/v1/suggest (page) through PCM's client: not answered by the service")

    # /v1/suggest, card
    card = {"kind": "kpi", "name": "Cluster Performance"}
    raw = client._post_raw(url + "/v1/suggest", {"facts": PAGE_FACTS, "card": card}, 20)
    if "question" in raw and not isinstance(raw["question"], (str, type(None))):
        problems.append("/v1/suggest (card): 'question' is not a string")
    if client.card_service(url, PAGE_FACTS, card, 20)["source"] != "service":
        problems.append("/v1/suggest (card) through PCM's client: not answered by the service")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repos", type=Path, default=Path(__file__).resolve().parents[2],
                        help="folder that holds the clones agent-e2 and private-cloud-manager (default: next to this repository)")
    args = parser.parse_args()
    agent_e2, pcm = args.repos / "agent-e2", args.repos / "private-cloud-manager"
    for repo in (agent_e2, pcm):
        if not repo.is_dir():
            print(f"ERROR: {repo} not found. Clone it, or pass --repos.")
            return 2
    port = free_port()
    try:
        proc = start_service(agent_e2, port)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        return 2
    try:
        problems = run(f"http://127.0.0.1:{port}", load_pcm_client(pcm))
    finally:
        proc.terminate()
        proc.wait(timeout=10)
    for p in problems:
        print(f"FAIL {p}")
    print(f"C3 Agent E2 API: 4 endpoints called with PCM's client, {len(problems)} difference(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
