---
name: add-feature
description: Add or extend behavior only after updating the relevant spec, tests, and eval dataset entries.
---

# Add A Feature

## Workflow
1. Confirm the target spec exists in `docs/specs/`.
2. Update or add eval cases in `evals/datasets/spec_compliance.jsonl`.
3. Add tests that fail first.
4. Implement the change in `src/`.
5. Run `./harness/tools/sandboxes/test_runner.sh`.

See `CHECKLIST.md` for the gate sequence.
