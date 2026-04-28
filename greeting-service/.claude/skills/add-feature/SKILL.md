---
name: add-feature
description: Add or extend behavior only after updating the relevant spec, tests, and eval dataset entries.
---

# Add A Feature

## Workflow
1. Confirm the target spec exists in `docs/specs/`, or add it from `docs/specs/template.md` before touching code.
2. Review `docs/architecture/invariants.md`, relevant ADRs, and `docs/validation/traceability-matrix.md`.
3. Add or update eval cases in `evals/datasets/spec_compliance.jsonl` and any relevant regression dataset.
4. Add tests that fail first at the narrowest useful layer.
5. Implement the change in `src/`.
6. Update traceability, runbooks, or orchestration metadata if the change affects those surfaces.
7. Run `./harness/tools/sandboxes/test_runner.sh`.

Use `CHECKLIST.md` as the completion gate, not just a reminder list.
