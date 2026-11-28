# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Check C5: the model gateway answers the model Agent E2 is set to (R-WS-008).

Sends one short question to the model named in agent-e2's harness/service_config.yaml, through the gateway named there,
with the key in the environment variable AI_GATEWAY_API_KEY, and expects an answer with text. The gateway is a third-party
service, so this proves only that the configured model answers. A model that does not exist fails and names its ID.

Exit 0: the model answered, or the check was not run (it prints "NOT RUN", as the name checks do, so a pipeline
without the key stays green and no one reads it as passed). Exit 1: the model did not answer. Exit 2: the repository is missing.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

QUESTION = "Reply with one word: ready."


def post(url: str, key: str, body: dict) -> tuple[int, dict]:
    req = urllib.request.Request(url, json.dumps(body).encode(),
                                 {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except ValueError:
            return e.code, {}


def check(gateway: str, model: str, key: str, send=post) -> list[str]:
    """The differences: [] when the model answered with text. The key is never part of a message."""
    try:
        status, data = send(gateway.rstrip("/") + "/chat/completions", key,
                            {"model": model, "messages": [{"role": "user", "content": QUESTION}], "max_tokens": 16})
    except (OSError, ValueError) as e:
        return [f"the gateway could not be reached for model '{model}': {type(e).__name__}"]
    if status != 200:
        return [f"model '{model}' did not answer: HTTP {status}"]
    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return [f"model '{model}' answered without a message"]
    return [] if isinstance(text, str) and text.strip() else [f"model '{model}' answered with no text"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repos", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    config = args.repos / "agent-e2" / "harness" / "service_config.yaml"
    if not config.is_file():
        print(f"NOT RUN C5 Model gateway: {config} not found")
        return 2
    key = os.environ.get("AI_GATEWAY_API_KEY", "")
    if not key:
        print("NOT RUN C5 Model gateway: AI_GATEWAY_API_KEY is not set")
        return 0
    cfg = yaml.safe_load(config.read_text())
    problems = check(cfg["gateway"], cfg["model"], key)
    for p in problems:
        print(f"FAIL {p}")
    print(f"C5 Model gateway: model '{cfg['model']}', {len(problems)} difference(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
