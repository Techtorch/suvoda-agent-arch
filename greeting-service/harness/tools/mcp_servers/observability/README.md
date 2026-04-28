# Observability MCP Server

This directory documents the contract for observability tools exposed to agents
over MCP.

## Intended Responsibilities

- Read orchestration traces from `harness/observability/`.
- Surface validation outcomes from tests, linters, drift checks, and evals.
- Summarize incident bundles and feedback-loop artifacts.
- Expose enough structure for monitoring and incident agents to reason over
  previous runs.

## Expected Tool Surface

- `observability.latest_trace()`
- `observability.trace(task_id)`
- `observability.latest_summary()`
- `observability.validation_events()`
- `observability.incident_bundle()`

## Design Constraints

- The server must preserve stable field names from `trace_schema.json`.
- Read operations should be deterministic and side-effect free.
- Returned payloads should be concise enough to fit inside agent context
  windows.

## Current State

The repo stores the trace format and example outputs today. A concrete MCP
server can be added later as a thin wrapper around those artifacts.
