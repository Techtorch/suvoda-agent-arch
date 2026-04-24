# ADR 0003: Ship Guides And Sensors With The Feature

## Status
Accepted

## Context
In an agentic environment, code without surrounding guidance and validation
degrades quickly. The workshop depends on making this visible.

## Decision
Behavior changes are not complete until the corresponding guides and sensors
are updated in the same change.

## Consequences
- Specs, tests, evals, and linters evolve together.
- The repo demonstrates continuous development rather than deferred validation.
