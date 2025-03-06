#!/bin/bash

# Enable strict error handling
set -e  # Exit on first error
set -o pipefail  # Prevent errors in pipelines from being masked
set -u  # Treat unset variables as an error

# Define the test files
TEST_FILES=("tests/test_main.py" "tests/test_image_processing.py")

# Run pytest on all test files
echo "🔍 Running tests..."
pytest -v "${TEST_FILES[@]}"

# Capture exit status of pytest
EXIT_STATUS=$?

# Display result message
if [ $EXIT_STATUS -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed. Check logs above."
fi

# Exit with pytest's exit status
exit $EXIT_STATUS
