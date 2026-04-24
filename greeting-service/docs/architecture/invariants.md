# Invariants

These properties must hold for every change to the demo repository.

1. `/hello` responses are always valid UTF-8 JSON.
2. The service only accepts `en`, `es`, and `fr`.
3. Service code in `src/` makes no outbound network client calls.
4. Every shipped spec has matching entries in the spec compliance dataset.

Enforcement:
- 1 — `tests/properties/test_invariants.py`
- 2 — `tests/unit/test_greeter.py` and `tests/integration/test_endpoint.py`
- 3 — `harness/sensors/linters/architectural_rules.py`
- 4 — `harness/sensors/linters/doc_sync_check.py`
