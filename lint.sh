#!/bin/sh

set -e

echo "Formatting..."
echo "--- Ruff ---"
ruff format llmkg
echo "--- isort ---"
isort llmkg

echo "Checking..."
echo "--- Flake8 ---"
flake8 llmkg
echo "--- pylint ---"
pylint llmkg
echo "--- mypy ---"
mypy llmkg
echo "--- Ruff ---"
ruff check llmkg
echo "--- pyright ---"
pyright llmkg
