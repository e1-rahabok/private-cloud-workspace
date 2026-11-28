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
import base64
import importlib.util
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
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


# Added in M3 (R-E2-007, R-E2-010, R-E2-011, R-E2-012, R-E2-016, R-E2-018, R-E2-022, R-E2-023), by name and type.
ANSWER_FIELDS_M3 = {"sources": (list,), "attachments_read": (list,), "missing_facts": (list,), "trace_id": (str,),
                    "elapsed_s": (int, float), "stage_seconds": (dict,), "usage": (dict,)}
USAGE_FIELDS = {"model_calls": (int,), "prompt_tokens": (int,), "completion_tokens": (int,)}
JOB_FIELDS = {"job": (str,), "state": (str,), "stage": (str, type(None)), "elapsed_s": (int, float), "updated_at": (str,)}
TRACE_FIELDS = {"trace_id": (str,), "model": (str,), "knowledge_commit": (str, type(None)), "files_read": (list,),
                "steps": (list,), "attachments": (list,)}
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64


def start_service(agent_e2: Path, port: int, env: dict | None = None, extra: list[str] | None = None) -> subprocess.Popen:
    proc = subprocess.Popen([sys.executable, str(agent_e2 / "harness" / "answer_service.py"), "--mock", "--port", str(port),
                             *(extra or [])],
                            cwd=agent_e2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            env={**os.environ, **(env or {})})
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


def http(url: str, path: str, body=None, headers=None, raw: bytes | None = None, timeout: int = 180):
    """One call; returns (status, JSON, headers). An HTTP error is a result, not an exception."""
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(url + path, data=data, headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read()), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}"), dict(e.headers)


def table_facts(agent_e2: Path) -> list[str]:
    """The fact names in the table of the docstring of answer_service.py (R-E2-017): column 2, each name in backticks."""
    doc = (agent_e2 / "harness" / "answer_service.py").read_text()
    rows = [r for r in doc.splitlines() if r.startswith("| ") and "---" not in r and not r.startswith("| Feature")]
    return sorted({n for r in rows for n in re.findall(r"`([^`]+)`", r.split("|")[2])})


def check_table(agent_e2: Path, pcm: Path, problems: list[str]) -> None:
    rows = [r for r in (agent_e2 / "harness" / "answer_service.py").read_text().splitlines()
            if r.startswith("| ") and "---" not in r and not r.startswith("| Feature")]
    if len(rows) < 7:
        problems.append(f"docstring table of facts: {len(rows)} feature rows, expected at least 7")
    frame = (pcm / "pcm" / "l2" / "spec" / "pages" / "frame.md").read_text()
    for name in table_facts(agent_e2):
        if name.split(".")[-1] not in frame:
            problems.append(f"docstring table of facts: '{name}' is not in PCM's frame.md")


def check_m3(url: str, agent_e2: Path, problems: list[str]) -> None:
    """The fields and refusals added in M3, called as isvara.io calls: a question, the role reader, a page, no facts."""
    page = "vsphere/technology/cpu/metrics/virtual-motherboard/ready"
    isvara = {"question": "And at what value is it a problem?", "role": "reader", "page": page,
              "history": [{"question": "What is CPU Ready?", "answer": "The time a vCPU waited."},
                          {"question": "Why does it rise?", "answer": "Contention."}]}
    status, out, _ = http(url, "/v1/answer", isvara)
    if status != 200:
        problems.append(f"/v1/answer (isvara.io shape): status {status}")
        return
    check_fields("/v1/answer (isvara.io shape)", out, {**ANSWER_FIELDS, **ANSWER_FIELDS_M3}, problems)
    check_fields("/v1/answer usage", out.get("usage") or {}, USAGE_FIELDS, problems)
    if out.get("lead") != "":
        problems.append("/v1/answer (isvara.io shape): 'lead' is not empty")
    check_fields("/v1/answer topic", out.get("topic") or {}, TOPIC_FIELDS, problems)
    for src in out.get("sources") or []:
        path = agent_e2 / "knowledge" / f"{src.get('id')}.md"
        if not path.is_file():
            problems.append(f"/v1/answer sources: '{src.get('id')}' is no knowledge file")
            continue
        head = next((l for l in path.read_text().splitlines() if l.startswith("# ")), "")[2:].strip()
        if src.get("title") != head:
            problems.append(f"/v1/answer sources: title of '{src['id']}' is {src.get('title')!r}, its heading is {head!r}")
    # Missing facts, in the shape of PCM's live facts, without parts_hourly (R-E2-018).
    status, live, _ = http(url, "/v1/answer", {"question": "Why did it fall?", "facts": PAGE_FACTS})
    if status != 200 or "parts_hourly" not in (live.get("missing_facts") or []):
        problems.append("/v1/answer: facts without parts_hourly did not list it in missing_facts")
    # The job call (R-E2-007).
    status, job, _ = http(url, "/v1/answer", {**isvara, "async": True})
    if status != 202 or job.get("state") != "queued" or not job.get("job"):
        problems.append(f"/v1/answer async: status {status}, expected 202 with a queued job")
    else:
        end = {}
        for _ in range(240):
            _, end, _ = http(url, f"/v1/jobs/{job['job']}")
            if end.get("state") in ("done", "failed"):
                break
            time.sleep(0.5)
        check_fields("/v1/jobs", end, JOB_FIELDS, problems)
        if end.get("state") != "done":
            problems.append(f"/v1/jobs: the job ended {end.get('state')!r}, expected 'done'")
        else:
            check_fields("/v1/jobs result", end.get("result") or {}, {**ANSWER_FIELDS, **ANSWER_FIELDS_M3}, problems)
    # The trace (R-E2-023).
    status, trace, _ = http(url, f"/v1/traces/{out.get('trace_id')}")
    if status != 200:
        problems.append(f"/v1/traces: status {status}, expected 200")
    else:
        check_fields("/v1/traces", trace, TRACE_FIELDS, problems)
    # Refusals by status (R-E2-008, R-E2-014, R-E2-022).
    refusals = [
        ("page that is no file", 400, "/v1/answer", {"question": "q?", "page": "vsphere/no-such-file"}, None),
        ("attachment that is no image or CSV", 400, "/v1/answer",
         {"question": "q?", "attachments": [{"name": "a.pdf", "data": base64.b64encode(b"%PDF-1.4").decode()}]}, None),
        ("image declared as text", 400, "/v1/answer",
         {"question": "q?", "attachments": [{"name": "a.csv", "type": "text/csv", "data": base64.b64encode(PNG).decode()}]}, None),
        ("unknown job", 404, "/v1/jobs/nothing", None, None),
        ("unknown trace", 404, "/v1/traces/nothing", None, None),
        ("body above 40 MB", 413, "/v1/answer", None, b'{"question": "' + b"a" * (41 * 1024 * 1024) + b'"}'),
    ]
    for name, want, path, body, raw in refusals:
        got = http(url, path, body, raw=raw)[0]
        if got != want:
            problems.append(f"{path} ({name}): status {got}, expected {want}")
    # An attachment is read: a screenshot and a CSV return attachments_read (R-E2-012, R-E2-013).
    status, out, _ = http(url, "/v1/answer", {"question": "What does this show?", "attachments": [
        {"name": "chart.png", "data": base64.b64encode(PNG).decode()},
        {"name": "vm.csv", "data": base64.b64encode(b"vm,ready\nvm-1,3.1\n").decode()}]})
    if status != 200 or not isinstance(out.get("attachments_read"), list):
        problems.append(f"/v1/answer with attachments: status {status}, 'attachments_read' is not a list")


def check_guarded(agent_e2: Path, problems: list[str]) -> None:
    """A service with a secret and no room for jobs: 401 without the header, 429 with it (R-E2-024, R-E2-008)."""
    config = Path(tempfile.mkdtemp(prefix="c3-")) / "service_config.yaml"
    config.write_text((agent_e2 / "harness" / "service_config.yaml").read_text() + "\nmax_running_jobs: 0\nmax_queued_jobs: 0\n")
    port = free_port()
    proc = start_service(agent_e2, port, {"AGENT_E2_SECRET": "contract-check"}, ["--config", str(config)])
    try:
        url, body = f"http://127.0.0.1:{port}", {"question": "q?", "async": True}
        if http(url, "/v1/answer", body)[0] != 401:
            problems.append("/v1/answer without the secret: expected 401")
        if http(url, "/v1/health")[0] != 200:
            problems.append("/v1/health must answer without the secret")
        status, _, headers = http(url, "/v1/answer", body, {"Authorization": "Bearer contract-check"})
        if status != 429 or "Retry-After" not in headers:
            problems.append(f"/v1/answer async with no room: status {status}, expected 429 with Retry-After")
    finally:
        proc.terminate()
        proc.wait(timeout=10)


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
        check_table(agent_e2, pcm, problems)
        check_m3(f"http://127.0.0.1:{port}", agent_e2, problems)
    finally:
        proc.terminate()
        proc.wait(timeout=10)
    try:
        check_guarded(agent_e2, problems)
    except RuntimeError as e:
        problems.append(f"the guarded service did not start: {e}")
    for p in problems:
        print(f"FAIL {p}")
    print(f"C3 Agent E2 API: PCM's client on 4 endpoints, isvara.io's shape on the job, trace and refusal calls, {len(problems)} difference(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
