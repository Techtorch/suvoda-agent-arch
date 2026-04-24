"""Check that declared invariants still point to real enforcement artifacts."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INVARIANTS_PATH = ROOT / "docs" / "architecture" / "invariants.md"


def extract_invariants(text):
    return re.findall(r"^\d+\.\s+.+$", text, flags=re.MULTILINE)


def extract_enforcement_paths(text):
    collecting = False
    paths = []

    for line in text.splitlines():
        if line.strip() == "Enforcement:":
            collecting = True
            continue

        if not collecting:
            continue

        if not line.startswith("- "):
            continue

        paths.extend(re.findall(r"`([^`]+)`", line))

    return paths


def main():
    text = INVARIANTS_PATH.read_text()
    invariants = extract_invariants(text)
    enforcement_paths = extract_enforcement_paths(text)
    violations = []

    if not invariants:
        violations.append("No invariants found in docs/architecture/invariants.md")

    if len(enforcement_paths) < len(invariants):
        violations.append("Invariant doc declares more invariants than enforcement entries")

    for relative_path in enforcement_paths:
        candidate = ROOT / relative_path
        if not candidate.exists():
            violations.append(
                f"Invariant doc references missing enforcement artifact: {relative_path}"
            )

    report = {
        "invariant_count": len(invariants),
        "enforcement_paths": enforcement_paths,
        "status": "failed" if violations else "passed",
    }
    print(json.dumps(report, indent=2))

    for violation in violations:
        print(violation, file=sys.stderr)

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
