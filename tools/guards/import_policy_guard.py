#!/usr/bin/env python3
import ast
import sys
from pathlib import Path

FORBIDDEN_PREFIXES = (
    "planninghub.application",
    "planninghub.infra",
)


def is_forbidden(module_name: str) -> bool:
    return any(
        module_name == prefix or module_name.startswith(f"{prefix}.")
        for prefix in FORBIDDEN_PREFIXES
    )


def check_file(path: Path) -> list[tuple[Path, str]]:
    violations: list[tuple[Path, str]] = []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if is_forbidden(alias.name):
                    violations.append((path, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module and is_forbidden(node.module):
                violations.append((path, node.module))
    return violations


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    domain_root = repo_root / "planninghub" / "domain"
    if not domain_root.exists():
        return 0

    all_violations: list[tuple[Path, str]] = []
    for path in sorted(domain_root.rglob("*.py")):
        all_violations.extend(check_file(path))

    if all_violations:
        for path, module_name in all_violations:
            rel_path = path.relative_to(repo_root)
            print(f"ERROR: {rel_path}: forbidden import {module_name}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
