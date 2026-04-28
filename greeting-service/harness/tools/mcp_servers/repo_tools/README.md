# Repo Tools MCP Server

This directory documents the contract for repo-scoped tools that an agent
runtime can expose over MCP.

## Intended Responsibilities

- Search the repository for guides, specs, tests, and control-plane artifacts.
- Read file contents with stable paths so agents can cite exact contracts.
- Run deterministic repo-local checks in a sandboxed way.
- Return compact summaries for architecture, traceability, and validation data.

## Expected Tool Surface

- `repo.search(query, scope?)`
- `repo.read(path)`
- `repo.list(prefix)`
- `repo.run_check(name)`
- `repo.traceability(intent_or_path)`

## Design Constraints

- Tools must be read-mostly by default.
- Any write or execution action must be explicit and auditable.
- Responses should prefer repo-native paths over prose descriptions.
- The contract is runtime-agnostic so the same repo can work across agent hosts.

## Current State

The repository defines the interface first. A concrete MCP server can be added
later without changing the surrounding harness model.
