# Traceability Matrix

| Intent | Source Guide | Enforcement |
| --- | --- | --- |
| `/hello` returns UTF-8 JSON | `docs/architecture/invariants.md` | `tests/properties/test_invariants.py` |
| Only supported languages are accepted | `docs/specs/001-hello-endpoint.md` | `tests/unit/test_greeter.py`, `tests/integration/test_endpoint.py` |
| No outbound network clients | `docs/architecture/decisions/0002-no-outbound-network.md` | `harness/sensors/linters/architectural_rules.py` |
| Every shipped spec is measurable | `docs/architecture/decisions/0003-guides-and-sensors-first.md` | `harness/sensors/linters/doc_sync_check.py`, `evals/datasets/spec_compliance.jsonl` |

The point of the matrix is simple: every guide should map to a concrete check.
