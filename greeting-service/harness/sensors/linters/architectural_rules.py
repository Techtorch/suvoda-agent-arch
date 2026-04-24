"""Deterministic architectural checks for the workshop demo."""

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FORBIDDEN_IMPORTS = {"requests", "httpx", "aiohttp"}
LOG_METHODS = {"debug", "info", "warning", "error", "critical"}


def check_network_imports(src_file):
    tree = ast.parse(src_file.read_text())
    violations = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_name = alias.name.split(".")[0]
                if root_name in FORBIDDEN_IMPORTS or alias.name == "urllib.request":
                    violations.append(
                        f"{src_file}:{node.lineno}: forbidden import '{alias.name}'"
                    )

        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root_name = module.split(".")[0]
            if root_name in FORBIDDEN_IMPORTS:
                violations.append(
                    f"{src_file}:{node.lineno}: forbidden import from '{module}'"
                )

            if module == "urllib" and any(
                alias.name == "request" for alias in node.names
            ):
                violations.append(
                    f"{src_file}:{node.lineno}: forbidden import from 'urllib.request'"
                )

            if module == "urllib.request":
                violations.append(
                    f"{src_file}:{node.lineno}: forbidden import from 'urllib.request'"
                )

    return violations


def check_logging_calls(src_file):
    tree = ast.parse(src_file.read_text())
    violations = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if not isinstance(node.func, ast.Attribute):
            continue

        if node.func.attr not in LOG_METHODS:
            continue

        dynamic_args = [arg for arg in node.args if not isinstance(arg, ast.Constant)]
        if dynamic_args:
            violations.append(
                f"{src_file}:{node.lineno}: logging call includes dynamic positional data"
            )

    return violations


def main():
    violations = []
    for src_file in sorted((ROOT / "src").rglob("*.py")):
        violations.extend(check_network_imports(src_file))
        violations.extend(check_logging_calls(src_file))

    for violation in violations:
        print(violation, file=sys.stderr)

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
