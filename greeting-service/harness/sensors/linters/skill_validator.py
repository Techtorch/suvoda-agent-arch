"""Validate the minimal frontmatter contract for skill files."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = ROOT / ".claude" / "skills"
REQUIRED_KEYS = {"name", "description"}


def parse_frontmatter(path):
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    frontmatter = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return frontmatter

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()

    return None


def main():
    violations = []

    for skill_file in sorted(SKILL_DIR.rglob("SKILL.md")):
        frontmatter = parse_frontmatter(skill_file)
        if frontmatter is None:
            violations.append(f"{skill_file}: missing frontmatter block")
            continue

        missing = REQUIRED_KEYS - set(frontmatter)
        if missing:
            violations.append(
                f"{skill_file}: missing required keys {sorted(missing)}"
            )

    for violation in violations:
        print(violation, file=sys.stderr)

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
