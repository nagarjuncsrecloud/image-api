#!/bin/bash

# Enable strict error handling
set -euo pipefail

# Navigate to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"
echo "Changed directory to $PROJECT_DIR"

# Debug: Print directory structure to verify tests location
echo "Listing directory structure:"
find . -type d

# Set PYTHONPATH to the current directory
export PYTHONPATH="$PROJECT_DIR"
echo "PYTHONPATH set to $PYTHONPATH"

# Run pytest on the tests folder if it exists
if [ -d "tests" ]; then
    echo "Running tests..."
    if pytest -s -v tests/; then
        echo "All tests passed!"
    else
        echo "Some tests failed. Check logs above."
        exit 1
    fi
else
    echo "Tests folder not found!"
    exit 1
fi
