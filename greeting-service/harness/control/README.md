# Control Plane

This folder contains repo-native descriptions of how specialized agents
coordinate across the harness.

## Why It Lives Here

The claim here is that orchestration should be inspectable like code:
- humans can review it
- agents can load it
- changes are versioned
- the control layer can evolve with the product

## Files

- `orchestration.yaml` is the machine-readable map of the pipeline.
- `run_showcase_pipeline.py` is the runnable orchestrator for the showcase.
- `generated/` stores generated incident-learning bundles.

Read this alongside `docs/architecture/multi-agent-orchestration.md`.
