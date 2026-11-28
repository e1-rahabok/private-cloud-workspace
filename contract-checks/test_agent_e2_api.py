"""Planted breaks for check C3 (contract-checks/agent_e2_api.py, R-WS-001, T-WS-001b): a response that lacks a field PCM
reads, or holds it with another type, fails and names the endpoint and the field. The full check starts the real
service; these tests plant the break in a response without it. Run: python -m unittest discover -s contract-checks -p "test_*.py".
"""
import unittest

import agent_e2_api as c3

GOOD_ANSWER = {"type": "answer", "content": "x", "lead": "x", "questions": [], "files_read": [], "computed": [],
               "topic": None, "model": "m", "knowledge_commit": None}


class PlantedBreaks(unittest.TestCase):
    def fields(self, out, fields=c3.ANSWER_FIELDS):
        problems: list[str] = []
        c3.check_fields("/v1/answer", out, fields, problems)
        return problems

    def test_a_good_answer_passes(self):
        self.assertEqual(self.fields(GOOD_ANSWER), [])

    def test_a_missing_field_fails_and_names_it(self):
        out = dict(GOOD_ANSWER)
        del out["lead"]
        self.assertEqual(self.fields(out), ["/v1/answer: response has no 'lead', which PCM reads"])

    def test_a_field_of_another_type_fails(self):
        problems = self.fields({**GOOD_ANSWER, "questions": "none"})
        self.assertTrue(problems and "'questions' is str" in problems[0], problems)


GOOD_M3 = {"sources": [], "attachments_read": [], "missing_facts": [], "trace_id": "t", "elapsed_s": 1.5, "stage_seconds": {},
           "usage": {"model_calls": 1, "prompt_tokens": 1, "completion_tokens": 1}}


class PlantedBreaksM3(PlantedBreaks):
    """The fields and refusals added in M3 (R-E2-019): each missing field or wrong type fails and names the field."""

    def test_the_new_fields_pass_when_present(self):
        self.assertEqual(self.fields(GOOD_M3, c3.ANSWER_FIELDS_M3), [])

    def test_each_new_field_missing_fails_and_names_it(self):
        for name in c3.ANSWER_FIELDS_M3:
            out = {k: v for k, v in GOOD_M3.items() if k != name}
            self.assertEqual(self.fields(out, c3.ANSWER_FIELDS_M3), [f"/v1/answer: response has no '{name}', which PCM reads"])

    def test_a_job_without_its_stage_fails(self):
        out = {"job": "j", "state": "running", "elapsed_s": 1, "updated_at": "t"}
        self.assertEqual(self.fields(out, c3.JOB_FIELDS), ["/v1/answer: response has no 'stage', which PCM reads"])

    def test_a_usage_count_of_another_type_fails(self):
        problems = self.fields({"model_calls": "1", "prompt_tokens": 1, "completion_tokens": 1}, c3.USAGE_FIELDS)
        self.assertTrue(problems and "'model_calls' is str" in problems[0], problems)


if __name__ == "__main__":
    unittest.main()
