import unittest

from evals.runners import llm_judge


class LLMJudgeTests(unittest.TestCase):
    def test_extract_dimensions_reads_numbered_rubric_items(self):
        dimensions = llm_judge.extract_dimensions(
            """
            1. Spec compliance
            2. Test coverage
            3. Invariant adherence
            """
        )
        self.assertEqual(
            ["Spec compliance", "Test coverage", "Invariant adherence"],
            dimensions,
        )

    def test_build_review_packet_uses_repo_rubric_and_eval_results(self):
        packet = llm_judge.build_review_packet()
        self.assertEqual("code_review.md", packet["rubric"])
        self.assertEqual(5, packet["dimension_count"])
        self.assertEqual("passed", packet["status"])
        self.assertGreaterEqual(packet["score"], packet["gate"])

    def test_render_markdown_report_lists_dimensions(self):
        report = llm_judge.render_markdown_report(
            {
                "rubric": "code_review.md",
                "score": 5.0,
                "gate": 4.5,
                "passed_cases": 10,
                "total_cases": 10,
                "status": "passed",
                "recommended_action": "Promote through deterministic gates.",
                "dimensions": ["Spec compliance", "Test coverage"],
            }
        )
        self.assertIn("# Critic Review Packet", report)
        self.assertIn("- Spec compliance", report)
        self.assertIn("- Test coverage", report)


if __name__ == "__main__":
    unittest.main()
