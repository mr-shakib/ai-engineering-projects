"""Run all tests across all projects."""

import subprocess
import sys
from pathlib import Path


def find_test_directories():
    """Find all test directories in the monorepo."""
    projects_dir = Path("projects")
    test_dirs = []

    if projects_dir.exists():
        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir():
                test_dir = project_dir / "tests"
                if test_dir.exists():
                    test_dirs.append(test_dir)

    return test_dirs


def run_tests(test_dir: Path, verbose: bool = False):
    """Run tests in a specific directory."""
    print(f"\n{'=' * 60}")
    print(f"Testing: {test_dir.parent.name}")
    print("=" * 60)

    cmd = ["pytest", str(test_dir)]

    if verbose:
        cmd.append("-v")

    # Add coverage if available
    cmd.extend(["--cov", str(test_dir.parent / "src"), "--cov-report", "term-missing"])

    result = subprocess.run(cmd)
    return result.returncode == 0


def main():
    """Run all tests."""
    verbose = "-v" in sys.argv or "--verbose" in sys.argv

    print("=" * 60)
    print("Running Tests for All Projects")
    print("=" * 60)

    test_dirs = find_test_directories()

    if not test_dirs:
        print("No test directories found.")
        return

    results = {}
    for test_dir in test_dirs:
        project_name = test_dir.parent.name
        results[project_name] = run_tests(test_dir, verbose)

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    all_passed = True
    for project_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{project_name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
