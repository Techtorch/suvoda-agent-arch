# Greeting Service Agent Instructions

## Project Purpose
This repository exists to showcase an agent-ready development harness.
The product is intentionally small: a single HTTP endpoint that returns a
greeting in one of three languages.

## Read First
1. `docs/architecture/overview.md`
2. `docs/architecture/invariants.md`
3. `docs/architecture/multi-agent-orchestration.md`
4. The relevant spec in `docs/specs/`
5. `docs/validation/traceability-matrix.md`

## Standard Workflow
1. Start from a spec or create one before changing behavior.
2. Keep changes narrow and explainable.
3. Update tests and eval datasets when behavior changes.
4. Run `./harness/tools/sandboxes/test_runner.sh` before handing work off.

## Architectural Ground Rules
- Use Python standard library only unless a new ADR approves a dependency.
- No outbound network client code in `src/`.
- Do not widen the API beyond the active spec.
- Treat docs, tests, evals, and sensors as part of the product.

## Stop And Ask A Human When
- You need to change an invariant.
- You need to add a dependency.
- You need to add persistence, authentication, or external integrations.

## Skills
Load the smallest relevant skill from `.claude/skills/`.
