# ADR 0001: Use Python Standard Library Only

## Status
Accepted

## Context
This repository is a compact architecture artifact. It needs to be
understandable quickly, run almost anywhere, and keep attention on the harness
rather than framework configuration.

## Decision
Use Python and the standard library for the application and the harness.

## Consequences
- Setup stays light.
- The example remains portable.
- Some conveniences from external packages are intentionally omitted.
