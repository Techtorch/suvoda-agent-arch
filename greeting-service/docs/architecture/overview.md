# Architecture Overview

This repository demonstrates a tiny application inside a deliberately visible
delivery harness.

## The Product
- `src/main.py` exposes the HTTP interface.
- `src/greeter.py` holds request validation and response construction.
- `src/formats.py` stores the language templates.

## The Guides
- `AGENTS.md` is the root operating guide.
- `docs/architecture/` captures stable system intent.
- `docs/architecture/multi-agent-orchestration.md` shows how specialized
  agents coordinate across the repo.
- `docs/specs/` defines feature-level behavior.
- `.claude/skills/` provides task-specific workflows on demand.

## The Sensors
- `tests/` checks behavior directly.
- `evals/` scores spec compliance against a reusable dataset.
- `harness/sensors/linters/` enforces architectural rules and doc quality.
- `harness/sensors/drift_detectors/` checks that the declared invariants still
  map to real enforcement artifacts.

## Continuous Development Loop
1. A guide declares intent.
2. A small code change implements the intent.
3. Sensors check the result immediately.
4. CI repeats the same gate on every pull request.
5. New failures become new guides or new sensors.

## Control Plane
- `harness/control/orchestration.yaml` is the machine-readable pipeline map.
- The repo therefore shows not just the code and harness, but also the
  orchestration contract between agents.
