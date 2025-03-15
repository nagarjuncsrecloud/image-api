#!/bin/bash

# Enable strict error handling
set -euo pipefail

# Navigate to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"
echo "Changed directory to $PROJECT_DIR"

# Set PYTHONPATH to the current directory
export PYTHONPATH="$PROJECT_DIR"
echo "PYTHONPATH set to $PYTHONPATH"

# Run pytest on all test files within the tests directory
echo "Running tests..."
if pytest -s -v tests/; then
    echo "All tests passed!"
else
    echo "Some tests failed. Check logs above."
    exit 1
fi
