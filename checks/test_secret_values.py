"""Planted breaks for checks/secret_values.py (R-WS-011, T-WS-011a). Run: python -m unittest discover -s checks -p "test_*.py".

Each planted token is joined at run time, so this file never holds one whole and no scanner flags it."""
import subprocess
import tempfile
import unittest
from pathlib import Path

import secret_values as scan

GITHUB = "gh" + "p_" + "Ab3" * 12
ANTHROPIC = "sk" + "-ant-" + "x9Y" * 10
AWS = "AK" + "IA" + "Q7RZ" * 4
SLACK = "xo" + "xb-" + "1234567890-abc"
VERCEL = "vc" + "k_" + "Zz9" * 8
KEY = "-----BEGIN " + "RSA PRIVATE KEY-----"
PASSWORD = "Pr0d" + "Pass!42"


def clone_with(files: dict[str, str]) -> tempfile.TemporaryDirectory:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    return tmp


class PlantedSecrets(unittest.TestCase):
    def test_each_kind_fails(self):
        files = {"a.md": f"token {GITHUB}\n", "b.py": f"KEY = '{ANTHROPIC}'\n", "c.txt": f"{AWS}\n",
                 "d.js": f"const s = '{SLACK}'\n", "e.env.md": f"VERCEL={VERCEL}\n", "f.pem.md": f"{KEY}\n",
                 "g.ps1": f"$password = '{PASSWORD}'\n", "h.json": f'{{"api_key": "{PASSWORD}"}}\n'}
        with clone_with(files) as tmp:
            problems = scan.problems_in("agent-e2", Path(tmp))
        self.assertEqual(sorted(p.split(":")[1].strip() for p in problems), sorted(files))

    def test_the_report_never_prints_the_value(self):
        with clone_with({"a.md": f"token {GITHUB}\n", "b.ps1": f"$password = '{PASSWORD}'\n"}) as tmp:
            problems = scan.problems_in("agent-e2", Path(tmp))
        self.assertEqual(len(problems), 2)
        self.assertFalse(any(GITHUB in p or PASSWORD in p for p in problems))

    def test_placeholders_and_references_pass(self):
        with clone_with({"a.md": 'password = "..."\napi_key: "<your key>"\ntoken = "${{ secrets.BLOB }}"\n',
                         "b.py": 'pwd="test-password"\npassword = "changeme123"\n',
                         "c.csv": "vcenter01,443,svc,VMware1!VMware1!\n",
                         "d.md": "the token is read from AI_GATEWAY_API_KEY; disk-latency-sk-metrics\n"}) as tmp:
            self.assertEqual(scan.problems_in("agent-e2", Path(tmp)), [])


if __name__ == "__main__":
    unittest.main()
