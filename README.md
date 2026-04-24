# TechTorch Agent Architecture Showcase

This repository contains a compact, shareable architecture showcase for
AI-native software delivery. The main implementation lives in
[`greeting-service/`](./greeting-service), where a small HTTP service is wrapped
in a visible harness of guides, specs, sensors, evals, orchestration, and
observability.

## Repository Contents

- [`greeting-service/`](./greeting-service)
  The runnable reference implementation, including the application,
  multi-agent control plane, validation layer, and architecture docs.
- [`greeting-service/README.md`](./greeting-service/README.md)
  Full technical walkthrough of the system, flow, structure, and file-level
  responsibilities.
- [`harness-repo-structure (1).md`](./harness-repo-structure%20%281%29.md)
  Reference repo structure and explanatory notes for the harness design.
- [`suvoda-workshop-narrative.html`](./suvoda-workshop-narrative.html)
  Narrative and chapter outline for the accompanying architecture workshop.

## Start Here

For the full implementation and documentation, open:

- [`greeting-service/README.md`](./greeting-service/README.md)
- [`greeting-service/docs/architecture/overview.md`](./greeting-service/docs/architecture/overview.md)
- [`greeting-service/docs/architecture/multi-agent-orchestration.md`](./greeting-service/docs/architecture/multi-agent-orchestration.md)

## What The Showcase Includes

- Root operating guide in `AGENTS.md`
- Executable specs in `docs/specs/`
- Product code in `src/`
- Tests and invariant checks in `tests/`
- Eval datasets, rubrics, and runners in `evals/`
- Deterministic sensors in `harness/sensors/`
- Runnable orchestration in `harness/control/`
- Runtime traces in `harness/observability/`
- CI gates in `.github/workflows/`

## Quick Run

```bash
cd greeting-service
python3 -m src.main
```

For the full walkthrough, commands, and architecture explanation, use the
README inside `greeting-service/`.
