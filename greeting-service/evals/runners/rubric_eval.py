"""Deterministic spec compliance evaluator for the workshop demo."""

import argparse
import json
from pathlib import Path

from src.greeter import build_response

ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT / "evals" / "datasets" / "spec_compliance.jsonl"
RESULTS_PATH = ROOT / "evals" / "results" / "latest_spec_compliance.json"


def load_cases():
    cases = []
    for raw_line in DATASET_PATH.read_text().splitlines():
        if raw_line.strip():
            cases.append(json.loads(raw_line))
    return cases


def evaluate_case(case):
    status_code, payload = build_response(case.get("name"), case.get("lang"))
    passed = (
        status_code == case["expected_status"]
        and payload == case["expected_payload"]
    )

    return {
        "spec_id": case["spec_id"],
        "input": {"name": case.get("name"), "lang": case.get("lang")},
        "passed": passed,
        "actual_status": status_code,
        "actual_payload": payload,
    }


def score_results(results):
    passed = sum(1 for result in results if result["passed"])
    total = len(results)
    pass_rate = passed / total if total else 0.0
    return round(pass_rate * 5, 2), passed, total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", type=float, default=4.0)
    args = parser.parse_args()

    cases = load_cases()
    results = [evaluate_case(case) for case in cases]
    score, passed, total = score_results(results)

    summary = {
        "score": score,
        "gate": args.gate,
        "passed_cases": passed,
        "total_cases": total,
        "status": "passed" if score >= args.gate else "failed",
    }
    RESULTS_PATH.write_text(
        json.dumps({"summary": summary, "results": results}, indent=2, ensure_ascii=False)
    )
    print(json.dumps(summary, indent=2))

    return 0 if score >= args.gate else 1


if __name__ == "__main__":
    raise SystemExit(main())
