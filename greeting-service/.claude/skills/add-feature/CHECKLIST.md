# Add Feature Checklist

- Spec exists in `docs/specs/` and the out-of-scope section is explicit.
- Acceptance criteria map to concrete unit, integration, or property checks.
- Any behavior change updates `docs/validation/traceability-matrix.md`.
- Any invariant or ADR impact is reviewed. If intent changes, stop for human approval.
- Eval dataset coverage exists for changed behavior and regression-sensitive paths.
- Tests fail before implementation and pass after implementation.
- Product code stays within declared scope and does not widen the API accidentally.
- Runbooks or architecture docs are updated if operating behavior changes.
- Orchestration metadata is updated if agent responsibilities or handoffs change.
- Full gate passes locally with `./harness/tools/sandboxes/test_runner.sh`.
