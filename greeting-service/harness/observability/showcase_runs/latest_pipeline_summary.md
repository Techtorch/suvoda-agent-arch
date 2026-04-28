# Showcase Pipeline Summary

- Task ID: `greeting-service-showcase-incident-20260428160305`
- Scenario: `incident`
- Request: Add or validate the hello endpoint within the declared harness constraints.
- Final status: `warning`

## Stage Results
- `intake`: `passed` — Captured request: Add or validate the hello endpoint within the declared harness constraints.
- `planner`: `passed` — Primary planning pass: loaded 4 repo guides and produced 3 work items.
- `design`: `passed` — Loaded spec template and active spec; found 4 acceptance criteria.
- `build`: `passed` — Validated 3 build artifacts under src/.
- `test`: `passed` — Discovered 16 tests and 10 spec compliance eval cases.
- `critic`: `passed` — Loaded critic rubric with 5 dimensions; score 5.0/5.0 against gate 4.5 (10/10 cases passed).
- `code_review`: `passed` — Loaded architectural reviewer with 4 review questions.
- `security`: `passed` — No violations found.
- `compliance`: `passed` — doc_sync_check=passed | invariant_check=passed
- `cicd`: `passed` — Full gate passed via ./harness/tools/sandboxes/test_runner.sh.
- `release`: `passed` — Release agent loaded deploy.md and rollback.md as operating context.
- `docs`: `passed` — Docs agent loaded update-docs skill and traceability matrix from .claude/skills/update-docs/SKILL.md and docs/validation/traceability-matrix.md.
- `deployed`: `passed` — Deployment checkpoint reached; monitoring can now inspect runtime behavior.
- `monitoring`: `warning` — Monitoring agent loaded trace schema with required fields ['task_id', 'status', 'gate_results']. Injected incident signal for feedback-loop walkthrough.
- `incident`: `passed` — Incident signal converted into a reusable harness-learning bundle. Bundle written to harness/control/generated/latest_incident_bundle.json.
- `planner_feedback`: `passed` — Feedback loop: loaded 4 repo guides and produced 3 work items.
