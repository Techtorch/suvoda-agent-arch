# TechTorch Agent Architecture Showcase

This repository is a simple, shareable example of how to build software with
AI agents in a controlled way.

The actual app is very small. It is just a greeting service that returns a
message like "Hello, Workshop!" in a few languages. The interesting part is not
the app itself. The interesting part is everything around it: the instructions,
specs, tests, checks, orchestration, and trace files that help AI agents work
safely and predictably.

This repo is built to answer a practical question:

**If AI can help write code, what needs to exist around that AI so the work is
clear, reviewable, and safe to ship?**

## What You Will Find Here

- [`greeting-service/`](./greeting-service)
  This is the main project. It contains the small app and all of the supporting
  files that explain how agents should work on it.
- [`greeting-service/README.md`](./greeting-service/README.md)
  This is the detailed walkthrough. It explains the repo structure, the flow
  between agents, what each important file does, and how to run the showcase.

## The Big Idea

This repo is built around one simple model:

```text
Agent = Model + Harness
```

That means:

- The **model** is the part that reasons and generates output.
- The **harness** is everything that keeps that output useful and safe.
- The harness includes instructions, rules, tests, quality checks, and
  feedback loops.

Without the harness, an agent is just generating text or code.
With the harness, an agent can work inside a real software process.

## Why The App Is Small

The app in this repo is intentionally tiny so the architecture is easy to see.
If the business logic were large and complex, it would distract from the main
point.

The repo is designed so a reader can quickly understand:

- what the product does
- what the agent is allowed to do
- what checks must pass
- how failures get turned into stronger future checks

## What The Showcase Includes

- `AGENTS.md`
  The main operating guide for agents. This is the first place an agent should
  look to understand the project.
- `docs/specs/`
  Structured feature specs. These say what the software should do in a clear,
  testable way.
- `src/`
  The product code for the greeting service.
- `tests/`
  Unit, integration, and property-style tests that check the behavior.
- `evals/`
  Datasets, rubrics, and runners used to measure whether the system still
  behaves as expected.
- `harness/sensors/`
  Hard checks that look for rule violations or documentation drift.
- `harness/control/`
  The control plane that describes and runs the multi-agent flow.
- `harness/observability/`
  Trace and summary outputs that show what happened during a pipeline run.
- `.github/workflows/`
  CI workflows that repeat the same checks in automation.

## Start Here

If you want the quickest way into the repo, open these files in order:

1. [`greeting-service/README.md`](./greeting-service/README.md)
2. [`greeting-service/docs/architecture/overview.md`](./greeting-service/docs/architecture/overview.md)
3. [`greeting-service/docs/architecture/multi-agent-orchestration.md`](./greeting-service/docs/architecture/multi-agent-orchestration.md)

## Quick Run

Start the service:

```bash
cd greeting-service
python3 -m src.main
```

This launches the small greeting app on your machine.

If you want the fuller architecture walkthrough, use the README inside
`greeting-service/`.

## What This Repo Is Really Demonstrating

At a high level, this repository shows four practical ideas:

1. AI agents need clear instructions, not just a prompt.
2. Good software work needs rules and checks that are stored in the repo.
3. Agent workflows should be visible and reviewable, not hidden in a tool.
4. When something goes wrong, the answer should be to improve the system, not
   just retry the prompt and hope for the best.
