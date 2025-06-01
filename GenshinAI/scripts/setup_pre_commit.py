#!/usr/bin/env python3
"""
Setup script for pre-commit hooks.

This script:
1. Installs pre-commit hooks from .pre-commit-config.yaml
2. Creates a Git alias 'force-commit' that allows committing even when hooks fail
"""

import subprocess
import sys


def run_command(command, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)

    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)

    if check and result.returncode != 0:
        sys.exit(result.returncode)

    return result


def main():
    """Set up pre-commit hooks and git aliases."""
    print("Setting up pre-commit hooks...")

    # Install pre-commit if not already installed
    try:
        subprocess.run(
            ["pre-commit", "--version"],
            check=True,
            capture_output=True,
        )
        print("pre-commit is already installed")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Installing pre-commit...")
        run_command("pip install pre-commit")

    # Install the hooks
    print("\nInstalling pre-commit hooks...")
    run_command("pre-commit install")

    # Create git alias for force-commit
    print("\nCreating git alias for force committing...")
    run_command('git config --local alias.force-commit "commit --no-verify"')

    print("\n✅ Setup complete!")
    print("\nYou can now use pre-commit hooks normally with 'git commit'")
    print("If you need to bypass the hooks, use: git force-commit -m 'Your message'")
    print("\nTo manually run pre-commit on all files: pre-commit run --all-files")


if __name__ == "__main__":
    main()
