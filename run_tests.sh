#!/bin/bash

# Enable strict error handling
set -euo pipefail

# Navigate to the project directory (one level up from the script location)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"
echo "Changed directory to $PROJECT_DIR"

# Detect the correct tests folder path
if [ -d "./image-api/tests" ]; then
    TESTS_DIR="./image-api/tests"
elif [ -d "./tests" ]; then
    TESTS_DIR="./tests"
else
    echo "❌ Tests folder not found!"
    exit 1
fi
echo "Tests directory found at $TESTS_DIR"

# Set PYTHONPATH to the image-api directory
export PYTHONPATH="$PROJECT_DIR/image-api"
echo "PYTHONPATH set to $PYTHONPATH"

# Run pytest on the detected tests folder
echo "Running tests..."
if pytest -s -v "$TESTS_DIR"; then
    echo "All tests passed!"
else
    echo "Some tests failed. Check logs above."
    exit 1
fi
