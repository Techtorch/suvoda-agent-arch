"""Check that shipped specs are well formed and measurable."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC_DIR = ROOT / "docs" / "specs"
DATASET_PATH = ROOT / "evals" / "datasets" / "spec_compliance.jsonl"
REQUIRED_HEADINGS = [
    "## Intent",
    "## Inputs",
    "## Output",
    "## Acceptance Criteria",
]


def collect_specs():
    specs = {}
    for path in sorted(SPEC_DIR.glob("[0-9][0-9][0-9]-*.md")):
        spec_id = path.stem.split("-", 1)[0]
        specs[spec_id] = path
    return specs


def load_dataset_ids():
    dataset_ids = set()
    violations = []
    for line_number, raw_line in enumerate(DATASET_PATH.read_text().splitlines(), start=1):
        if not raw_line.strip():
            continue

        record = json.loads(raw_line)
        spec_id = record.get("spec_id")
        if not spec_id:
            violations.append(
                f"{DATASET_PATH}:{line_number}: missing spec_id in dataset record"
            )
            continue

        dataset_ids.add(spec_id)

    return dataset_ids, violations


def main():
    specs = collect_specs()
    dataset_ids, violations = load_dataset_ids()

    for spec_id, path in specs.items():
        text = path.read_text()
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                violations.append(f"{path}: missing heading '{heading}'")

        if spec_id not in dataset_ids:
            violations.append(
                f"{path}: no matching eval entries in {DATASET_PATH.name}"
            )

    for dataset_id in sorted(dataset_ids):
        if dataset_id not in specs:
            violations.append(
                f"{DATASET_PATH}: dataset references unknown spec_id '{dataset_id}'"
            )

    for violation in violations:
        print(violation, file=sys.stderr)

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
