"""Offline critic helpers for rubric-driven review scoring."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from evals.runners import rubric_eval

ROOT = Path(__file__).resolve().parents[2]
RUBRIC_DIR = ROOT / "evals" / "rubrics"
DEFAULT_RUBRIC = "code_review.md"


def load_rubric(name: str = DEFAULT_RUBRIC) -> str:
    rubric_path = RUBRIC_DIR / name
    return rubric_path.read_text()


def extract_dimensions(rubric_text: str) -> list[str]:
    dimensions: list[str] = []
    for line in rubric_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("1. ", "2. ", "3. ", "4. ", "5. ")):
            dimensions.append(stripped.split(". ", 1)[1])
    return dimensions


def build_review_packet(
    gate: float = 4.5,
    rubric_name: str = DEFAULT_RUBRIC,
) -> dict[str, Any]:
    rubric_text = load_rubric(rubric_name)
    dimensions = extract_dimensions(rubric_text)
    results = [rubric_eval.evaluate_case(case) for case in rubric_eval.load_cases()]
    score, passed_cases, total_cases = rubric_eval.score_results(results)
    status = "passed" if score >= gate else "failed"

    return {
        "rubric": rubric_name,
        "dimensions": dimensions,
        "dimension_count": len(dimensions),
        "score": score,
        "gate": gate,
        "passed_cases": passed_cases,
        "total_cases": total_cases,
        "status": status,
        "recommended_action": (
            "Promote through deterministic gates."
            if status == "passed"
            else "Revise the change before promotion."
        ),
    }


def render_markdown_report(packet: dict[str, Any]) -> str:
    lines = [
        "# Critic Review Packet",
        "",
        f"- Rubric: `{packet['rubric']}`",
        f"- Score: `{packet['score']}` / `5.0`",
        f"- Gate: `{packet['gate']}`",
        f"- Cases passed: `{packet['passed_cases']}/{packet['total_cases']}`",
        f"- Status: `{packet['status']}`",
        f"- Recommendation: {packet['recommended_action']}",
        "",
        "## Dimensions",
    ]
    lines.extend(f"- {dimension}" for dimension in packet["dimensions"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", type=float, default=4.5)
    parser.add_argument("--rubric", default=DEFAULT_RUBRIC)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args(argv)

    packet = build_review_packet(gate=args.gate, rubric_name=args.rubric)
    if args.format == "markdown":
        print(render_markdown_report(packet), end="")
    else:
        print(json.dumps(packet, indent=2))

    return 0 if packet["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
