"""Planted breaks for checks/lab_addresses.py (R-WS-010, T-WS-010a). Run: python -m unittest discover -s checks -p "test_*.py"."""
import subprocess
import tempfile
import unittest
from pathlib import Path

import lab_addresses as lab


def clone_with(files: dict[str, str]) -> tempfile.TemporaryDirectory:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    return tmp


class PlantedLabAddresses(unittest.TestCase):
    def test_a_private_address_fails_in_each_range(self):
        with clone_with({"a.md": "the VM at https://10.99.1.29\n", "b.ps1": "$h = '172.20.0.4'\n",
                         "c.json": '{"host": "192.168.1.10"}\n', "d.md": "the file `vcf-ops-10.99.1.81.xml`\n"}) as tmp:
            problems = lab.problems_in("agent-e2", Path(tmp), [])
        self.assertEqual(sorted(p.split(":")[1].strip() for p in problems), ["a.md", "b.ps1", "c.json", "d.md"])

    def test_the_report_never_prints_the_address(self):
        with clone_with({"a.md": "https://10.99.1.29\n"}) as tmp:
            problems = lab.problems_in("agent-e2", Path(tmp), [])
        self.assertEqual(len(problems), 1)
        self.assertNotIn("10.99.1.29", problems[0])

    def test_examples_versions_and_public_addresses_pass(self):
        with clone_with({"a.md": "example VM 10.20.1.9, network 10.20.0.0/24\n",
                         "b.md": "pillow 10.4.0, espree 10.4.0, ESXi 8.0.3\n",
                         "c.md": "docs 192.0.2.10, DNS 8.8.8.8, OID 1.3.6.1.4.1\n"}) as tmp:
            self.assertEqual(lab.problems_in("agent-e2", Path(tmp), []), [])

    def test_a_listed_private_name_fails(self):
        with clone_with({"a.md": "ssh to labhost77 now\n", "b.md": "nothing here\n"}) as tmp:
            problems = lab.problems_in("agent-e2", Path(tmp), ["labhost77"])
        self.assertEqual([p.split(":")[1].strip() for p in problems], ["a.md"])

    def test_the_books_are_outside_the_rule(self):
        with clone_with({"content/books/part-3.md": "subnet 10.0.3.0\n", "spec/a.md": "subnet 10.0.3.0\n"}) as tmp:
            problems = lab.problems_in("isvara", Path(tmp), [])
        self.assertEqual([p.split(":")[1].strip() for p in problems], ["spec/a.md"])


if __name__ == "__main__":
    unittest.main()
