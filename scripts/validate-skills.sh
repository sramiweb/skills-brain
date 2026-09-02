#!/usr/bin/env bash
# Canonical local validation entry point for Skills Brain v2.1.

set -euo pipefail

python tooling/validate.py --all
python -m compileall -q tooling adapters
pytest -q
python tooling/evaluator.py
python tooling/catalog.py

echo "Skills Brain validation completed successfully."
