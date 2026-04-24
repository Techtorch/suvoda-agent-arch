# Deploy Runbook

This demo is designed for local execution and pull request validation.

## Local Demo Deployment
1. Run `python3 -m src.main`
2. Verify `GET /health`
3. Verify `GET /hello?name=Workshop&lang=en`

## Pull Request Gate
Run `./harness/tools/sandboxes/test_runner.sh` before asking for review.
