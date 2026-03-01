#!/usr/bin/env python3
"""Detect files for code simplification scope.

Usage:
    python detect_scope.py                          # Modified files only
    python detect_scope.py --staged                 # Only staged files
    python detect_scope.py --all                    # Include untracked
    python detect_scope.py --repo                   # All tracked source files
    python detect_scope.py --dir src/auth           # All source files in directory
    python detect_scope.py --ext .ts,.tsx,.py       # Filter by extensions

Output:
    One file path per line, sorted by file size (largest first).

Exit codes:
    0 - Files found
    1 - No files found
    2 - Not in a git repository
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_git(*args: str) -> list[str]:
    """Run a git command and return non-empty output lines."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        return []


def is_git_repo() -> bool:
    """Check if the current directory is inside a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_modified_files(staged_only: bool = False, include_all: bool = False) -> list[str]:
    """Get list of modified files from git.

    Priority:
    1. Staged files (git diff --cached)
    2. Unstaged modifications (git diff)
    3. Untracked files (if --all)
    """
    files: set[str] = set()

    if staged_only or not include_all:
        # Staged changes
        staged = run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
        files.update(staged)

    if not staged_only:
        # Unstaged changes
        unstaged = run_git("diff", "--name-only", "--diff-filter=ACMR")
        files.update(unstaged)

    if include_all:
        # Untracked files
        untracked = run_git("ls-files", "--others", "--exclude-standard")
        files.update(untracked)

    return sorted(files)


def filter_by_extensions(files: list[str], extensions: list[str]) -> list[str]:
    """Filter files by extension."""
    ext_set = {ext if ext.startswith(".") else f".{ext}" for ext in extensions}
    return [f for f in files if Path(f).suffix in ext_set]


def get_tracked_source_files(directory: str | None = None) -> list[str]:
    """Get all tracked source files in the repo, optionally filtered to a directory."""
    args = ["ls-files"]
    if directory:
        args.append(directory)
    return run_git(*args)


# Common non-source extensions to exclude in repo-wide scans
EXCLUDED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".bmp",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".pdf", ".zip", ".tar", ".gz", ".br",
    ".lock", ".map", ".min.js", ".min.css",
    ".sqlite", ".db", ".DS_Store",
}

EXCLUDED_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", "__pycache__",
    ".venv", "venv", "vendor", "coverage", ".turbo", ".cache",
}


def filter_source_files(files: list[str]) -> list[str]:
    """Exclude binary, generated, and vendor files."""
    result = []
    for f in files:
        path = Path(f)
        if path.suffix.lower() in EXCLUDED_EXTENSIONS:
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        result.append(f)
    return result


def filter_existing(files: list[str]) -> list[str]:
    """Filter to only files that exist on disk."""
    return [f for f in files if Path(f).is_file()]


def sort_by_size_desc(files: list[str]) -> list[str]:
    """Sort files by size, largest first (most complex files likely largest)."""
    def file_size(f: str) -> int:
        try:
            return Path(f).stat().st_size
        except OSError:
            return 0
    return sorted(files, key=file_size, reverse=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect files for simplification scope")
    parser.add_argument("--staged", action="store_true", help="Only staged files")
    parser.add_argument("--all", action="store_true", help="Include untracked files")
    parser.add_argument("--repo", action="store_true", help="All tracked source files in repo")
    parser.add_argument("--dir", type=str, help="All source files in a specific directory")
    parser.add_argument("--ext", type=str, help="Comma-separated extensions to filter (e.g., .ts,.tsx,.py)")
    args = parser.parse_args()

    if not is_git_repo():
        print("ERROR: Not inside a git repository", file=sys.stderr)
        sys.exit(2)

    # Determine scope
    if args.repo:
        files = get_tracked_source_files()
        files = filter_source_files(files)
        scope = "entire repository"
    elif args.dir:
        files = get_tracked_source_files(args.dir)
        files = filter_source_files(files)
        scope = f"directory: {args.dir}"
    else:
        files = get_modified_files(staged_only=args.staged, include_all=args.all)
        scope = "modified files"

    files = filter_existing(files)

    if args.ext:
        extensions = [e.strip() for e in args.ext.split(",")]
        files = filter_by_extensions(files, extensions)

    if not files:
        print(f"No files found ({scope})", file=sys.stderr)
        sys.exit(1)

    # Sort largest first — most complex files get attention first
    files = sort_by_size_desc(files)

    # Output summary to stderr, file list to stdout
    print(f"Found {len(files)} file(s) [{scope}]:", file=sys.stderr)
    for f in files:
        print(f)


if __name__ == "__main__":
    main()
