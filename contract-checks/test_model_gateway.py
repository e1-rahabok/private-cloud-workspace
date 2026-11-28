"""Planted breaks for check C5 (contract-checks/model_gateway.py, R-WS-001, T-WS-008a): a model that answers passes; a
model that does not exist, an answer with no text and an unreachable gateway fail and name the model. Without the key the
check prints NOT RUN and does not print a pass. Run: python -m unittest discover -s contract-checks -p "test_*.py".
"""
import os
import subprocess
import sys
import unittest
from pathlib import Path

import model_gateway as c5

OK = (200, {"choices": [{"message": {"content": "ready"}}]})


class PlantedBreaks(unittest.TestCase):
    def run_check(self, reply, model="google/gemma-4-31b-it"):
        return c5.check("https://gateway.example/v1", model, "key-123", lambda url, key, body: reply)

    def test_a_model_that_answers_passes(self):
        self.assertEqual(self.run_check(OK), [])

    def test_a_model_that_does_not_exist_fails_and_names_it(self):
        problems = self.run_check((404, {"error": "no such model"}), "google/no-such-model")
        self.assertEqual(problems, ["model 'google/no-such-model' did not answer: HTTP 404"])

    def test_an_answer_with_no_text_fails(self):
        self.assertTrue(self.run_check((200, {"choices": [{"message": {"content": "  "}}]})))
        self.assertTrue(self.run_check((200, {})))

    def test_an_unreachable_gateway_fails_without_the_key(self):
        def down(url, key, body):
            raise OSError("down")
        problems = c5.check("https://gateway.example/v1", "m", "key-123", down)
        self.assertTrue(problems and "key-123" not in problems[0])

    def test_without_the_key_the_check_is_not_run(self):
        env = {k: v for k, v in os.environ.items() if k != "AI_GATEWAY_API_KEY"}
        here = Path(__file__).resolve().parent
        out = subprocess.run([sys.executable, str(here / "model_gateway.py"), "--repos", str(here.parents[1])],
                             env=env, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertIn("NOT RUN", out.stdout)
        self.assertNotIn("difference(s)", out.stdout)


if __name__ == "__main__":
    unittest.main()
