---
name: update-docs
description: Update guides, specs, ADRs, or runbooks so the repository context stays aligned with the code.
---

# Update Docs

## Workflow
1. Change the source guide.
2. Update traceability if the change affects enforcement.
3. Run `python3 -m harness.sensors.linters.doc_sync_check`.
