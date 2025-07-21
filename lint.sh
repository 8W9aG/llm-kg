#!/bin/sh

set -e

echo "Formatting..."
echo "--- Ruff ---"
ruff format llmkgext
echo "--- isort ---"
isort llmkgext

echo "Checking..."
echo "--- Flake8 ---"
flake8 llmkgext
echo "--- pylint ---"
pylint llmkgext
echo "--- mypy ---"
mypy llmkgext
echo "--- Ruff ---"
ruff check llmkgext
echo "--- pyright ---"
pyright llmkgext
