# ADR 0002: No Outbound Network Calls

## Status
Accepted

## Context
The repository is meant to show agentic development patterns, not service
integration. Outbound calls add noise, increase failure modes, and dilute the
architecture lesson.

## Decision
Application code in `src/` must not import or use outbound network clients.

## Consequences
- The app stays deterministic and easy to test.
- The architectural rules linter can enforce this decision directly.
