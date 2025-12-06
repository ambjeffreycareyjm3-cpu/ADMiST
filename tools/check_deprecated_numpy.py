#!/usr/bin/env python3
"""Simple checker for deprecated NumPy API usage.

This script scans repository Python files for usages of known deprecated
NumPy APIs (a conservative list). If any matches are found it prints them
and exits with non-zero status so CI or a pre-commit hook can fail.

Add patterns here as deprecations are discovered.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Patterns to search for (regex) - add more deprecated symbols as needed
DEPRECATED_PATTERNS = [
    r"\bnp\.trapz\b",
    r"\bnumpy\.trapz\b",
    r"\bnp\.asscalar\b",
    r"\bnumpy\.asscalar\b",
    r"\bnp\.bool\b",
    r"\bnp\.int\b",
    r"\bnp\.float\b",
    r"\bnp\.object\b",
]

compiled = [re.compile(p) for p in DEPRECATED_PATTERNS]


def scan_file(path: Path):
    text = path.read_text(encoding="utf8", errors="ignore")
    hits = []
    for i, line in enumerate(text.splitlines(), start=1):
        for pat in compiled:
            if pat.search(line):
                hits.append((i, line.strip()))
    return hits


def main():
    py_files = [
        p for p in ROOT.rglob("*.py") if "venv" not in p.parts and ".git" not in p.parts
    ]
    # Don't scan this checker script itself
    this_file = Path(__file__).resolve()
    py_files = [p for p in py_files if p.resolve() != this_file]
    problems = {}
    for p in py_files:
        hits = scan_file(p)
        if hits:
            problems[p.relative_to(ROOT)] = hits

    if problems:
        print("\nDeprecated NumPy API usage detected:")
        for f, hits in problems.items():
            print(f"\n  {f}:")
            for lineno, line in hits:
                print(f"    {lineno:4d}: {line}")
        print(
            "\nPlease replace deprecated APIs (e.g. use np.trapezoid instead of np.trapz)."
        )
        return 2

    print("No deprecated NumPy API usage found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
