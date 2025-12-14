"""Lint and format all code in the monorepo."""

import subprocess
import sys
from pathlib import Path


def run_black(path: str = ".") -> bool:
    """Run Black code formatter."""
    print("Running Black...")
    result = subprocess.run(["black", path])
    return result.returncode == 0


def run_isort(path: str = ".") -> bool:
    """Run isort import sorter."""
    print("\nRunning isort...")
    result = subprocess.run(["isort", path])
    return result.returncode == 0


def run_ruff(path: str = ".", fix: bool = True) -> bool:
    """Run Ruff linter."""
    print("\nRunning Ruff...")
    cmd = ["ruff", "check", path]
    if fix:
        cmd.append("--fix")
    result = subprocess.run(cmd)
    return result.returncode == 0


def run_mypy(paths: list = None) -> bool:
    """Run mypy type checker."""
    print("\nRunning mypy...")
    if paths is None:
        paths = ["projects/"]

    # Check if paths exist
    valid_paths = [p for p in paths if Path(p).exists()]

    if not valid_paths:
        print("No valid paths to type check.")
        return True

    result = subprocess.run(["mypy"] + valid_paths)
    return result.returncode == 0


def main():
    """Run all linting and formatting tools."""
    print("=" * 60)
    print("Code Quality Check")
    print("=" * 60)

    # Check if we should skip fixing
    check_only = "--check" in sys.argv

    results = {
        "Black": run_black("."),
        "isort": run_isort("."),
        "Ruff": run_ruff(".", fix=not check_only),
        "mypy": run_mypy(),
    }

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    all_passed = True
    for tool, passed in results.items():
        status = "✓ PASSED" if passed else "✗ ISSUES FOUND"
        print(f"{tool}: {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n✓ All checks passed!")
        sys.exit(0)
    else:
        print("\n✗ Some issues found. Please fix them.")
        if not check_only:
            print("Some issues were auto-fixed. Review changes.")
        sys.exit(1)


if __name__ == "__main__":
    main()
