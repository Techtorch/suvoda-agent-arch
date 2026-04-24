import json
import tempfile
import unittest
from pathlib import Path

from harness.control.run_demo_pipeline import (
    INCIDENT_SCENARIO_ID,
    apply_incident_learning,
    build_incident_learning_bundle,
    load_simple_yaml,
)


class DemoPipelineTests(unittest.TestCase):
    def test_manifest_loads_expected_agents(self):
        manifest = load_simple_yaml(
            Path("harness/control/orchestration.yaml")
        )
        agents = manifest["pipeline"]["agents"]
        self.assertIn("planner", agents)
        self.assertIn("build", agents)
        self.assertIn("incident", agents)

    def test_incident_learning_bundle_can_be_applied_idempotently(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "harness/sensors/linters").mkdir(parents=True)
            (root / "docs/architecture/decisions").mkdir(parents=True)
            (root / "evals/datasets").mkdir(parents=True)
            (root / "evals/datasets/regression_cases.jsonl").write_text("")

            bundle = build_incident_learning_bundle(root)
            first_write = apply_incident_learning(root, bundle)
            second_write = apply_incident_learning(root, bundle)

            self.assertTrue(first_write)
            self.assertEqual([], second_write)

            regression_lines = (
                root / "evals/datasets/regression_cases.jsonl"
            ).read_text().splitlines()
            records = [json.loads(line) for line in regression_lines if line.strip()]
            self.assertEqual([INCIDENT_SCENARIO_ID], [item["scenario"] for item in records])


if __name__ == "__main__":
    unittest.main()
