# Rollback Runbook

This service has no persistent state. Rollback is simply a code rollback.

## Procedure
1. Revert the offending change.
2. Run `./harness/tools/sandboxes/test_runner.sh`.
3. Re-open the pull request only when the full gate passes.
