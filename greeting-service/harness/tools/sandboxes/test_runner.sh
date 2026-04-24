#!/usr/bin/env bash
set -euo pipefail

python3 -m harness.sensors.linters.architectural_rules
python3 -m harness.sensors.linters.doc_sync_check
python3 -m harness.sensors.linters.skill_validator
python3 -m unittest discover -s tests -v
python3 -m evals.runners.rubric_eval --gate 4.5
python3 -m harness.sensors.drift_detectors.invariant_check
