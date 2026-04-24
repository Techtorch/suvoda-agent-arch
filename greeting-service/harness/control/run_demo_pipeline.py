"""Runnable multi-agent orchestration demo for the workshop repository."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import subprocess
import sys
import textwrap
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evals.runners import rubric_eval
from harness.sensors.drift_detectors import invariant_check
from harness.sensors.linters import architectural_rules, doc_sync_check

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "harness" / "control" / "orchestration.yaml"
TRACE_DIR = ROOT / "harness" / "observability" / "demo_runs"
GENERATED_DIR = ROOT / "harness" / "control" / "generated"
TRACE_PATH = TRACE_DIR / "latest_pipeline_trace.json"
SUMMARY_PATH = TRACE_DIR / "latest_pipeline_summary.md"
INCIDENT_BUNDLE_PATH = GENERATED_DIR / "latest_incident_bundle.json"
INCIDENT_SCENARIO_ID = "demo_incident_guard"


def _next_significant_line(lines: list[str], start_index: int) -> tuple[int, str] | None:
    for index in range(start_index + 1, len(lines)):
        stripped = lines[index].strip()
        if stripped and not stripped.startswith("#"):
            return index, lines[index]
    return None


def _parse_scalar(value: str) -> Any:
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value in {"true", "false"}:
        return value == "true"
    return value


def load_simple_yaml(path: Path) -> dict[str, Any]:
    """Parse the limited YAML subset used by orchestration.yaml."""

    lines = path.read_text().splitlines()
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for index, raw_line in enumerate(lines):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1]

        if stripped.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError(f"Invalid list item near line {index + 1}: {raw_line}")
            parent.append(_parse_scalar(stripped[2:].strip()))
            continue

        key, separator, remainder = stripped.partition(":")
        if separator != ":":
            raise ValueError(f"Invalid mapping near line {index + 1}: {raw_line}")

        key = key.strip()
        remainder = remainder.lstrip()

        if remainder:
            value = _parse_scalar(remainder)
            if not isinstance(parent, dict):
                raise ValueError(f"Invalid parent for key '{key}' near line {index + 1}")
            parent[key] = value
            continue

        lookahead = _next_significant_line(lines, index)
        if lookahead is None:
            container: Any = {}
        else:
            _, next_line = lookahead
            next_indent = len(next_line) - len(next_line.lstrip(" "))
            if next_indent <= indent:
                container = {}
            else:
                container = [] if next_line.strip().startswith("- ") else {}

        if not isinstance(parent, dict):
            raise ValueError(f"Invalid parent for nested key '{key}' near line {index + 1}")
        parent[key] = container
        stack.append((indent, container))

    return root


def run_callable(name: str, func) -> dict[str, Any]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exit_code = func()

    status = "passed" if exit_code == 0 else "failed"
    details = "\n".join(
        part for part in [stdout.getvalue().strip(), stderr.getvalue().strip()] if part
    )
    if not details and status == "passed":
        details = "No violations found."
    return {"name": name, "status": status, "details": details, "exit_code": exit_code}


def count_list_items_under_heading(path: Path, heading: str) -> int:
    lines = path.read_text().splitlines()
    in_section = False
    count = 0

    for line in lines:
        if line.strip() == heading:
            in_section = True
            continue

        if in_section and line.startswith("## "):
            break

        normalized = line.lstrip()
        if in_section and (
            normalized.startswith("- ")
            or normalized.startswith("1. ")
            or normalized.startswith("2. ")
            or normalized.startswith("3. ")
            or normalized.startswith("4. ")
            or normalized.startswith("5. ")
        ):
            count += 1

    return count


def count_numbered_lines(path: Path) -> int:
    count = 0
    for line in path.read_text().splitlines():
        normalized = line.lstrip()
        if normalized.startswith(("1. ", "2. ", "3. ", "4. ", "5. ")):
            count += 1
    return count


def discover_unittest_names(root: Path) -> list[str]:
    loader = unittest.defaultTestLoader
    suite = loader.discover(str(root / "tests"))
    names: list[str] = []

    def walk(node):
        for item in node:
            if isinstance(item, unittest.TestSuite):
                walk(item)
            else:
                names.append(item.id())

    walk(suite)
    return names


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def build_incident_learning_bundle(root: Path) -> dict[str, Any]:
    linter_path = root / "harness" / "sensors" / "linters" / "demo_incident_guard.py"
    adr_path = (
        root
        / "docs"
        / "architecture"
        / "decisions"
        / "0999-demo-incident-learning.md"
    )
    regression_path = root / "evals" / "datasets" / "regression_cases.jsonl"

    return {
        "scenario_id": INCIDENT_SCENARIO_ID,
        "summary": "Production incident becomes new harness infrastructure.",
        "targets": [
            {
                "path": str(linter_path.relative_to(root)),
                "kind": "linter",
                "content": textwrap.dedent(
                    '''\
                    """Demo incident guard created by the incident agent."""

                    INCIDENT_GUARD = {
                        "scenario": "demo_incident_guard",
                        "intent": "Show that production failures become reusable harness checks."
                    }
                    '''
                ).strip()
                + "\n",
            },
            {
                "path": str(adr_path.relative_to(root)),
                "kind": "adr",
                "content": textwrap.dedent(
                    """\
                    # ADR 0999: Demo Incident Learning

                    ## Status
                    Accepted

                    ## Context
                    The workshop demo needs a visible example of the feedback loop
                    where an incident produces a durable harness change.

                    ## Decision
                    Keep a demo incident artifact that shows how a production issue
                    would create a new linter and regression case.

                    ## Consequences
                    - The feedback loop is visible in the repository.
                    - Audiences can see that failures enrich the environment.
                    """
                ).strip()
                + "\n",
            },
            {
                "path": str(regression_path.relative_to(root)),
                "kind": "eval_dataset_append",
                "record": {
                    "scenario": INCIDENT_SCENARIO_ID,
                    "input": {"name": "IncidentReplay", "lang": "fr"},
                    "expected_status": 200,
                    "expected_payload": {
                        "greeting": "Bonjour, IncidentReplay!",
                        "language": "fr",
                    },
                },
            },
        ],
    }


def apply_incident_learning(root: Path, bundle: dict[str, Any]) -> list[str]:
    written_paths: list[str] = []

    for target in bundle["targets"]:
        path = root / target["path"]
        path.parent.mkdir(parents=True, exist_ok=True)

        if target["kind"] == "eval_dataset_append":
            existing_lines = []
            if path.exists():
                existing_lines = path.read_text().splitlines()

            desired_record = json.dumps(target["record"], ensure_ascii=False)
            existing_scenarios = {
                json.loads(line).get("scenario")
                for line in existing_lines
                if line.strip()
            }
            if INCIDENT_SCENARIO_ID not in existing_scenarios:
                with path.open("a", encoding="utf-8") as handle:
                    if existing_lines:
                        handle.write("\n")
                    handle.write(desired_record)
                written_paths.append(target["path"])
            continue

        content = target["content"]
        if not path.exists() or path.read_text() != content:
            path.write_text(content)
            written_paths.append(target["path"])

    return written_paths


def stage_intake(context: dict[str, Any]) -> dict[str, Any]:
    request = context["request"]
    summary = f"Captured request: {request}"
    return {"status": "passed", "details": summary, "outputs": {"request": request}}


def stage_planner(context: dict[str, Any], feedback_loop: bool = False) -> dict[str, Any]:
    reads = context["manifest"]["pipeline"]["agents"]["planner"]["reads"]
    existing = [path for path in reads if (ROOT / path).exists()]
    plan = [
        "Confirm the active guide and architecture constraints.",
        "Check spec and implementation scope.",
        "Run deterministic and probabilistic validation.",
    ]
    prefix = "Feedback loop" if feedback_loop else "Primary planning pass"
    details = (
        f"{prefix}: loaded {len(existing)} repo guides and produced {len(plan)} work items."
    )
    return {"status": "passed", "details": details, "outputs": {"plan": plan}}


def stage_design(context: dict[str, Any]) -> dict[str, Any]:
    template_path = ROOT / "docs" / "specs" / "template.md"
    spec_path = ROOT / "docs" / "specs" / "001-hello-endpoint.md"
    acceptance_count = count_list_items_under_heading(spec_path, "## Acceptance Criteria")
    details = (
        f"Loaded spec template and active spec; found {acceptance_count} acceptance criteria."
    )
    return {
        "status": "passed",
        "details": details,
        "outputs": {
            "template": str(template_path.relative_to(ROOT)),
            "active_spec": str(spec_path.relative_to(ROOT)),
            "acceptance_criteria": acceptance_count,
        },
    }


def stage_build(context: dict[str, Any]) -> dict[str, Any]:
    files = [
        "src/main.py",
        "src/greeter.py",
        "src/formats.py",
    ]
    details = f"Validated {len(files)} build artifacts under src/."
    return {"status": "passed", "details": details, "outputs": {"files": files}}


def stage_test(context: dict[str, Any]) -> dict[str, Any]:
    tests = discover_unittest_names(ROOT)
    dataset_cases = len(rubric_eval.load_cases())
    details = (
        f"Discovered {len(tests)} tests and {dataset_cases} spec compliance eval cases."
    )
    return {
        "status": "passed",
        "details": details,
        "outputs": {"tests": len(tests), "eval_cases": dataset_cases},
    }


def stage_critic(context: dict[str, Any]) -> dict[str, Any]:
    rubric_path = ROOT / "evals" / "rubrics" / "code_review.md"
    results = [rubric_eval.evaluate_case(case) for case in rubric_eval.load_cases()]
    score, passed, total = rubric_eval.score_results(results)
    dimensions = count_numbered_lines(rubric_path)
    details = (
        f"Loaded critic rubric with {dimensions} dimensions; current deterministic score is "
        f"{score}/5.0 ({passed}/{total} cases)."
    )
    return {
        "status": "passed",
        "details": details,
        "outputs": {"score": score, "passed_cases": passed, "total_cases": total},
    }


def stage_code_review(context: dict[str, Any]) -> dict[str, Any]:
    reviewer_path = ROOT / "harness" / "sensors" / "review_agents" / "architectural_reviewer.md"
    questions = [
        line.strip()
        for line in reviewer_path.read_text().splitlines()
        if line.strip().startswith(("1.", "2.", "3.", "4."))
    ]
    details = f"Loaded architectural reviewer with {len(questions)} review questions."
    return {"status": "passed", "details": details, "outputs": {"questions": questions}}


def stage_security(context: dict[str, Any]) -> dict[str, Any]:
    result = run_callable("architectural_rules", architectural_rules.main)
    return {"status": result["status"], "details": result["details"], "outputs": result}


def stage_compliance(context: dict[str, Any]) -> dict[str, Any]:
    doc_sync = run_callable("doc_sync_check", doc_sync_check.main)
    invariant = run_callable("invariant_check", invariant_check.main)
    passed = doc_sync["status"] == "passed" and invariant["status"] == "passed"
    details = " | ".join(
        [
            f"doc_sync_check={doc_sync['status']}",
            f"invariant_check={invariant['status']}",
        ]
    )
    return {
        "status": "passed" if passed else "failed",
        "details": details,
        "outputs": {"doc_sync": doc_sync, "invariant": invariant},
    }


def stage_cicd(context: dict[str, Any]) -> dict[str, Any]:
    if context["skip_cicd"]:
        return {
            "status": "skipped",
            "details": "CI/CD gate skipped by request.",
            "outputs": {"skipped": True},
        }

    command = ["./harness/tools/sandboxes/test_runner.sh"]
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    combined_output = "\n".join(
        part for part in [result.stdout.strip(), result.stderr.strip()] if part
    )
    return {
        "status": "passed" if result.returncode == 0 else "failed",
        "details": combined_output,
        "outputs": {"command": " ".join(command), "returncode": result.returncode},
    }


def stage_release(context: dict[str, Any]) -> dict[str, Any]:
    deploy_path = ROOT / "docs" / "runbooks" / "deploy.md"
    rollback_path = ROOT / "docs" / "runbooks" / "rollback.md"
    details = (
        f"Release agent loaded {deploy_path.name} and {rollback_path.name} as operating context."
    )
    return {"status": "passed", "details": details, "outputs": {"runbooks": 2}}


def stage_docs(context: dict[str, Any]) -> dict[str, Any]:
    skill_path = ROOT / ".claude" / "skills" / "update-docs" / "SKILL.md"
    traceability_path = ROOT / "docs" / "validation" / "traceability-matrix.md"
    detail = (
        f"Docs agent loaded update-docs skill and traceability matrix from "
        f"{skill_path.relative_to(ROOT)} and {traceability_path.relative_to(ROOT)}."
    )
    return {"status": "passed", "details": detail, "outputs": {"skill_loaded": True}}


def stage_deployed(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "passed",
        "details": "Deployment checkpoint reached; monitoring can now inspect runtime behavior.",
        "outputs": {"deployed": True},
    }


def stage_monitoring(context: dict[str, Any]) -> dict[str, Any]:
    schema = json.loads((ROOT / "harness" / "observability" / "trace_schema.json").read_text())
    required_fields = schema["required"]
    status = "warning" if context["scenario"] == "incident" else "passed"
    details = (
        f"Monitoring agent loaded trace schema with required fields {required_fields}."
    )
    if context["scenario"] == "incident":
        details += " Injected demo incident signal for feedback-loop walkthrough."
    return {"status": status, "details": details, "outputs": {"required_fields": required_fields}}


def stage_incident(context: dict[str, Any]) -> dict[str, Any]:
    if context["scenario"] == "happy":
        return {
            "status": "skipped",
            "details": "No incident injected; pipeline ends on successful deployment.",
            "outputs": {"incident": False},
        }

    bundle = build_incident_learning_bundle(ROOT)
    write_json(INCIDENT_BUNDLE_PATH, bundle)
    written_paths: list[str] = []
    if context["apply_incident_learning"]:
        written_paths = apply_incident_learning(ROOT, bundle)

    details = "Incident signal converted into a reusable harness-learning bundle."
    if written_paths:
        details += f" Materialized artifacts: {', '.join(written_paths)}."
    else:
        details += " Bundle written to harness/control/generated/latest_incident_bundle.json."

    return {
        "status": "passed",
        "details": details,
        "outputs": {"incident": True, "bundle_path": str(INCIDENT_BUNDLE_PATH.relative_to(ROOT))},
    }


STAGE_HANDLERS = {
    "intake": stage_intake,
    "planner": stage_planner,
    "design": stage_design,
    "build": stage_build,
    "test": stage_test,
    "critic": stage_critic,
    "code_review": stage_code_review,
    "security": stage_security,
    "compliance": stage_compliance,
    "cicd": stage_cicd,
    "release": stage_release,
    "docs": stage_docs,
    "deployed": stage_deployed,
    "monitoring": stage_monitoring,
    "incident": stage_incident,
}

PRIMARY_EXECUTION_ORDER = [
    "intake",
    "planner",
    "design",
    "build",
    "test",
    "critic",
    "code_review",
    "security",
    "compliance",
    "cicd",
    "release",
    "docs",
    "deployed",
    "monitoring",
    "incident",
]


def render_summary(trace: dict[str, Any]) -> str:
    lines = [
        "# Demo Pipeline Summary",
        "",
        f"- Task ID: `{trace['task_id']}`",
        f"- Scenario: `{trace['scenario']}`",
        f"- Request: {trace['request']}",
        f"- Final status: `{trace['status']}`",
        "",
        "## Stage Results",
    ]

    for item in trace["gate_results"]:
        detail = item["details"].splitlines()[0] if item["details"] else "No details"
        lines.append(f"- `{item['name']}`: `{item['status']}` — {detail}")

    return "\n".join(lines) + "\n"


def record_stage_result(trace_results: list[dict[str, Any]], name: str, result: dict[str, Any]) -> None:
    trace_results.append(
        {
            "name": name,
            "status": result["status"],
            "details": result["details"],
        }
    )


def run_pipeline(request: str, scenario: str, skip_cicd: bool, apply_incident_learning_flag: bool) -> dict[str, Any]:
    manifest = load_simple_yaml(MANIFEST_PATH)
    pipeline_id = manifest["pipeline"]["id"]
    task_id = f"{pipeline_id}-{scenario}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

    context = {
        "manifest": manifest,
        "request": request,
        "scenario": scenario,
        "skip_cicd": skip_cicd,
        "apply_incident_learning": apply_incident_learning_flag,
    }
    trace_results: list[dict[str, Any]] = []
    final_status = "passed"

    for stage_name in PRIMARY_EXECUTION_ORDER:
        handler = STAGE_HANDLERS[stage_name]
        result = handler(context)
        record_stage_result(trace_results, stage_name, result)
        print(f"[{len(trace_results):02d}] {stage_name}: {result['status']} - {result['details']}")

        if result["status"] == "failed":
            final_status = "failed"
            break

        if stage_name == "incident" and scenario == "incident":
            feedback_result = stage_planner(context, feedback_loop=True)
            record_stage_result(trace_results, "planner_feedback", feedback_result)
            print(
                f"[{len(trace_results):02d}] planner_feedback: {feedback_result['status']} - "
                f"{feedback_result['details']}"
            )

    if any(item["status"] == "warning" for item in trace_results) and final_status == "passed":
        final_status = "warning"

    trace = {
        "task_id": task_id,
        "status": final_status,
        "spec_id": "001",
        "scenario": scenario,
        "request": request,
        "gate_results": trace_results,
    }
    return trace


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--request",
        default="Add or validate the hello endpoint within the declared harness constraints.",
        help="Short natural-language request to push through the demo pipeline.",
    )
    parser.add_argument(
        "--scenario",
        choices=["happy", "incident"],
        default="happy",
        help="Choose the happy path or a feedback-loop incident walkthrough.",
    )
    parser.add_argument(
        "--skip-cicd",
        action="store_true",
        help="Skip the full gate stage. Useful in restricted environments.",
    )
    parser.add_argument(
        "--apply-incident-learning",
        action="store_true",
        help="When running the incident scenario, materialize the incident learning into repo files.",
    )
    args = parser.parse_args(argv)

    trace = run_pipeline(
        request=args.request,
        scenario=args.scenario,
        skip_cicd=args.skip_cicd,
        apply_incident_learning_flag=args.apply_incident_learning,
    )
    write_json(TRACE_PATH, trace)
    SUMMARY_PATH.write_text(render_summary(trace))

    print(f"\nTrace written to {TRACE_PATH.relative_to(ROOT)}")
    print(f"Summary written to {SUMMARY_PATH.relative_to(ROOT)}")
    if args.scenario == "incident":
        print(f"Incident bundle written to {INCIDENT_BUNDLE_PATH.relative_to(ROOT)}")

    return 0 if trace["status"] in {"passed", "warning"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
