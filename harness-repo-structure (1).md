# AI-Native Repository Structure

A reference layout for a production-grade harness. Built around a toy "greeting service" so the focus stays on the harness, not the domain logic.

The file tree below shows what actually lives in an agent-first repo. Every file has a purpose in the harness. Open any of them and you should be able to tell whether it's a **guide** (tells the agent what to do) or a **sensor** (checks what the agent did).

---

## Repository tree

```
greeting-service/
├── AGENTS.md                          # Root guide — the system prompt every agent reads first
├── README.md                          # Human-facing overview
├── CLAUDE.md                          # Claude Code-specific instructions (aliases AGENTS.md)
│
├── .claude/
│   ├── skills/                        # Progressive-disclosure capabilities
│   │   ├── add-feature/
│   │   │   ├── SKILL.md               # Metadata + core workflow
│   │   │   ├── CHECKLIST.md           # Step-by-step gate checks
│   │   │   └── examples/
│   │   │       └── reference-pr.md    # Known-good example
│   │   ├── fix-bug/
│   │   │   └── SKILL.md
│   │   ├── update-docs/
│   │   │   └── SKILL.md
│   │   └── write-test/
│   │       └── SKILL.md
│   │
│   └── commands/                      # Reusable slash commands
│       ├── review-pr.md
│       └── run-evals.md
│
├── docs/
│   ├── architecture/
│   │   ├── overview.md                # High-level system map
│   │   ├── decisions/                 # ADRs — architectural decision records
│   │   │   ├── 0001-use-python.md
│   │   │   ├── 0002-no-new-dependencies.md
│   │   │   └── 0003-greeting-formats.md
│   │   └── invariants.md              # What must never change
│   │
│   ├── specs/                         # Feature specs the agent executes against
│   │   ├── 001-hello-endpoint.md
│   │   ├── 002-multilingual-support.md
│   │   └── template.md
│   │
│   └── runbooks/                      # Operational procedures for agents
│       ├── deploy.md
│       └── rollback.md
│
├── src/
│   ├── __init__.py
│   ├── main.py                        # Entry point
│   ├── greeter.py                     # Core logic
│   └── formats.py                     # Greeting formats
│
├── tests/
│   ├── unit/
│   │   ├── test_greeter.py
│   │   └── test_formats.py
│   ├── integration/
│   │   └── test_endpoint.py
│   └── properties/
│       └── test_invariants.py         # Property-based tests
│
├── evals/                             # Sensor layer — how we measure agent output quality
│   ├── datasets/
│   │   ├── code_quality.jsonl
│   │   ├── spec_compliance.jsonl
│   │   └── regression_cases.jsonl
│   ├── rubrics/
│   │   ├── code_review.md
│   │   └── spec_compliance.md
│   ├── runners/
│   │   ├── llm_judge.py
│   │   └── rubric_eval.py
│   └── results/
│       └── .gitkeep
│
├── harness/                           # The infrastructure that makes agents reliable
│   ├── guides/                        # Pointers to where guides live
│   │   └── README.md
│   ├── sensors/
│   │   ├── linters/
│   │   │   ├── architectural_rules.py # Enforces ADR decisions
│   │   │   ├── doc_sync_check.py      # Fails if docs drift from code
│   │   │   └── skill_validator.py     # Validates SKILL.md structure
│   │   ├── drift_detectors/
│   │   │   └── invariant_check.py     # Runs nightly, flags entropy
│   │   └── review_agents/
│   │       └── architectural_reviewer.md
│   │
│   ├── tools/
│   │   ├── mcp_servers/               # MCP-compliant tool servers
│   │   │   ├── repo_tools/
│   │   │   └── observability/
│   │   └── sandboxes/
│   │       └── test_runner.sh
│   │
│   └── observability/
│       ├── logs_config.yaml
│       └── trace_schema.json
│
├── .github/
│   └── workflows/
│       ├── ci.yml                     # Linters + tests + evals on every PR
│       ├── nightly_drift.yml          # Runs drift detectors
│       └── eval_gate.yml              # Blocks merge if eval scores regress
│
├── pyproject.toml
├── .gitignore
└── .env.example
```

---

## What lives in each part of the harness

### Guides — what we tell the agent

**AGENTS.md** (root)
The single source of truth the agent reads at task start. Project purpose, architectural ground rules, what's off-limits, how to run tests, where to find specs, when to escalate to humans. Kept under 500 lines. If it grows beyond that, break it into referenced files.

**docs/architecture/invariants.md**
The short list of things that must never change — the greeting service always returns valid UTF-8, never logs user names, never makes outbound network calls. These are the deterministic guarantees the sensor layer enforces.

**docs/architecture/decisions/**
Architectural decision records (ADRs). Each one captures a decision, its context, and its consequences. The agent reads these to understand *why* the code is shaped the way it is — which prevents it from "fixing" things that were intentional.

**docs/specs/**
Structured specifications the agent executes against. Each spec defines what the feature is, what "correct" means, what the edge cases are, and what tests must pass. Spec-driven development in practice.

**.claude/skills/**
Reusable capabilities loaded on demand via progressive disclosure. Each `SKILL.md` has frontmatter (name, description) that's always in context, plus a body that only loads when the skill is triggered. Prevents context bloat while keeping dozens of capabilities available.

### Sensors — what checks the agent's work

**harness/sensors/linters/architectural_rules.py**
Deterministic enforcement of architectural invariants. If an ADR says "no new external dependencies without review," the linter blocks the PR when a new dependency appears. Probabilistic compliance becomes deterministic enforcement.

**harness/sensors/linters/doc_sync_check.py**
Fails the build if code changed but the corresponding doc didn't, or vice versa. Stops documentation drift that would poison future agent runs.

**harness/sensors/drift_detectors/invariant_check.py**
Runs nightly. Scans for inconsistencies in documentation, violations of architectural constraints, and silent entropy. Opens issues for agents to fix in the background. This is the "garbage collector" pattern — agents fighting decay continuously.

**evals/**
The measurement layer. Datasets of input/expected-output pairs, rubrics for LLM-as-judge evaluation, and runners that score agent output. Eval scores gate merges — if a change regresses code quality or spec compliance, CI blocks it.

**tests/properties/test_invariants.py**
Property-based tests that assert the invariants from `docs/architecture/invariants.md` hold for any input. Complements example-based tests.

### Tools — what the agent can act on

**harness/tools/mcp_servers/**
MCP-compliant tool servers expose capabilities to the agent — reading the repo, querying observability data, running sandboxed commands. Using MCP keeps us portable across agent runtimes rather than locked into one vendor's tool layer.

**harness/tools/sandboxes/test_runner.sh**
Isolated execution environment for running tests on agent-generated code. The agent can execute and observe results without affecting the working tree.

### Observability — what the agent can see about itself

**harness/observability/**
Trace schemas and log configuration that make agent runs inspectable. When the agent fails, humans and other agents can read the trace and diagnose why. Also fed back into the agent's own context so it can self-correct.

### CI — where guides and sensors come together

**.github/workflows/ci.yml**
On every PR: run linters, run tests, run evals. If any gate fails, the PR doesn't merge. This is the deterministic backstop that catches what the probabilistic layer missed.

**.github/workflows/nightly_drift.yml**
Runs drift detectors on a schedule. Opens issues, assigns them to agents, keeps the codebase coherent over time.

**.github/workflows/eval_gate.yml**
Blocks merge if eval scores regress below threshold. The production gate for agent-generated changes.

---

## Sample file contents

### AGENTS.md (abridged)

```markdown
# Greeting Service — Agent Instructions

## Project purpose
A minimal HTTP service that returns greetings in multiple languages.
Scope is deliberately tiny — this repo exists to demonstrate harness
patterns, not to solve a real greeting problem.

## Before you do anything
1. Read `docs/architecture/overview.md`
2. Check `docs/architecture/invariants.md` — these must never be violated
3. If a spec exists in `docs/specs/`, work from it; if not, ask

## How to run
- Tests: `pytest tests/`
- Linters: `python -m harness.sensors.linters`
- Evals: `python evals/runners/rubric_eval.py`

## Architectural ground rules
- No new external dependencies without an ADR in `docs/architecture/decisions/`
- No outbound network calls from the service
- No logging of user-provided content
- All new features require a spec + tests + eval dataset entries

## When to stop and ask
- Any change to files in `docs/architecture/invariants.md`
- Any change that touches more than 3 modules
- Any test that you can't make pass within 2 attempts

## Available skills
See `.claude/skills/` — skills load on demand when relevant.
```

### .claude/skills/add-feature/SKILL.md

```markdown
---
name: add-feature
description: Add a new feature to the greeting service following the spec-driven workflow. Use when the user requests a new capability or references a spec in docs/specs/.
---

# Add a feature

## Workflow
1. Locate or create the spec in `docs/specs/`
2. Add eval dataset entries in `evals/datasets/spec_compliance.jsonl`
3. Write failing tests in `tests/unit/` and `tests/integration/`
4. Implement in `src/`
5. Run the full gate: tests + linters + evals
6. If any gate fails, fix before opening the PR

See `CHECKLIST.md` for the full gate list.
See `examples/reference-pr.md` for a known-good example.
```

### docs/architecture/invariants.md

```markdown
# Invariants

These properties must hold for every change. The sensor layer enforces them.

1. All responses are valid UTF-8
2. No user-provided content appears in logs
3. No outbound network calls from `src/greeter.py`
4. Response latency < 100ms for any supported language
5. Every public function has a corresponding test

Enforcement:
- 1, 2, 3 — `harness/sensors/linters/architectural_rules.py`
- 4 — `tests/properties/test_invariants.py`
- 5 — `harness/sensors/linters/doc_sync_check.py`
```

### docs/specs/001-hello-endpoint.md

```markdown
# Spec 001 — Hello endpoint

## Intent
Expose a GET /hello endpoint that returns a greeting.

## Inputs
- Query parameter `name` (optional, string, max 50 chars)
- Query parameter `lang` (optional, enum: en, es, fr, default: en)

## Output
- 200 with JSON body: `{"greeting": "<string>"}`
- 400 if `name` exceeds 50 chars
- 400 if `lang` is not supported

## Acceptance criteria
- Unit tests cover all three input combinations + error cases
- Integration test hits the running endpoint
- Eval dataset includes 10 input/expected pairs in evals/datasets/spec_compliance.jsonl

## Out of scope
- Authentication
- Rate limiting
- Persistent storage
```

### evals/rubrics/code_review.md

```markdown
# Code review rubric

Score each agent-generated change on a 1–5 scale across these dimensions.
Used by `evals/runners/llm_judge.py`.

## Dimensions

**Spec compliance (1–5)**
Does the change implement what the spec describes, nothing more, nothing less?

**Test coverage (1–5)**
Are new code paths covered by tests? Do tests check edge cases called out in the spec?

**Invariant adherence (1–5)**
Does the change respect `docs/architecture/invariants.md`? Did any linter fail?

**Code clarity (1–5)**
Can a human reviewer understand the change in under 2 minutes?

**Blast radius (1–5, inverted)**
How many modules does the change touch? Smaller is better.

## Gate
Mean score < 4.0 → PR is blocked pending revision.
```

### harness/sensors/linters/architectural_rules.py

```python
"""
Architectural rules linter.
Enforces decisions recorded in docs/architecture/decisions/.
Runs in CI; failure blocks the PR.
"""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
FORBIDDEN_IMPORTS = {"requests", "urllib", "httpx"}  # no outbound network
ALLOWED_LOG_ARGS = {"level", "event", "duration_ms"}  # no user content

def check_no_network_imports(src_file: Path) -> list[str]:
    tree = ast.parse(src_file.read_text())
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in FORBIDDEN_IMPORTS:
                    violations.append(
                        f"{src_file}: forbidden import '{alias.name}' "
                        f"(see docs/architecture/decisions/0002)"
                    )
    return violations

def main() -> int:
    all_violations = []
    for py_file in (ROOT / "src").rglob("*.py"):
        all_violations.extend(check_no_network_imports(py_file))
    for v in all_violations:
        print(v, file=sys.stderr)
    return 1 if all_violations else 0

if __name__ == "__main__":
    sys.exit(main())
```

### .github/workflows/ci.yml

```yaml
name: CI
on: [pull_request]

jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install
        run: pip install -e ".[dev]"

      # Sensor layer — deterministic
      - name: Architectural rules
        run: python -m harness.sensors.linters.architectural_rules

      - name: Doc sync check
        run: python -m harness.sensors.linters.doc_sync_check

      - name: Skill validator
        run: python -m harness.sensors.linters.skill_validator

      # Tests
      - name: Unit tests
        run: pytest tests/unit/

      - name: Integration tests
        run: pytest tests/integration/

      - name: Property tests
        run: pytest tests/properties/

      # Sensor layer — probabilistic
      - name: Run evals
        run: python evals/runners/rubric_eval.py --gate 4.0
```

---

## How to read this repo in the workshop

The point isn't the greeting service — it's what surrounds it.

Walk the room through three views of the same repo:

**View 1 — Where the agent looks first.** `AGENTS.md`, the skills, the specs, the ADRs, the invariants. Everything the agent reads to know what to do. These are the guides.

**View 2 — Where the agent's work gets checked.** `tests/`, `evals/`, `harness/sensors/`, `.github/workflows/`. Everything that observes what the agent produced and blocks bad output. These are the sensors.

**View 3 — What compounds.** Notice that every sensor enforces something written in a guide. Every failure the team has hit has become a linter, an eval case, a property test, a new ADR. The harness accumulates. A new agent dropped into this repo on day 90 operates in a dramatically richer environment than one dropped in on day 1 — not because the model got better, but because the environment did.

This is what "every failure becomes infrastructure" looks like in a file tree.
