---
name: fix-bug
description: Fix a defect by reproducing it with a test first, then patching code and rerunning the full gate.
---

# Fix A Bug

## Workflow
1. Reproduce the issue in `tests/`.
2. Patch the smallest relevant module in `src/`.
3. Add an eval case if the bug changes external behavior.
4. Run the full gate.
