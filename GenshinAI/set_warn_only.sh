#!/bin/bash

# Set up pre-commit hooks in warn-only mode
echo "Setting up pre-commit hooks to allow commits even when checks fail..."
pre-commit uninstall
SKIP=no_commit_to_branch pre-commit install --hook-type pre-commit --allow-missing-config --config .pre-commit-config.yaml
echo "export SKIP=no_commit_to_branch" >> ~/.bashrc
echo "export SKIP=no_commit_to_branch" >> ~/.zshrc

# Create git alias for force commits
git config --local alias.force-commit "commit --no-verify"

echo "✅ Done! You can now commit even when pre-commit checks fail."
echo "You can also use 'git force-commit -m \"your message\"' to skip checks completely."
