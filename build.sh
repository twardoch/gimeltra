#!/usr/bin/env bash
# this_file: build.sh
# Lint, type-check, test, and build the distribution.
set -euo pipefail
cd "$(dirname "$0")"

uvx ruff check .
uvx ruff format --check .
uv run --extra dev mypy gimeltra
uv run --extra dev pytest --cov=gimeltra --cov-report=term-missing
uv build

echo "Built:"
ls -1 dist/
