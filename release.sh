#!/bin/bash
# release.sh - Release automation script for the savecode package.
# This script removes previous build artifacts, rebuilds the package,
# and uploads the new version to PyPI using Twine.
# update the version number in the savecode/savecode/__init__.py file and run this script to release the package to PyPI
#run using "bash release.sh"

# use: "python -m savecode.cli -r ." for testing of changes

set -e

# Automatically extract the version from savecode/__init__.py using a raw string literal for the regex
VERSION=$(python -c "import re; f = open('savecode/__init__.py'); s = f.read(); f.close(); m = re.search(r\"__version__\s*=\s*[\\\"']([^\\\"']+)[\\\"']\", s); print(m.group(1) if m else '0.0.0')")
echo "Using version: $VERSION"

# Remove previous build artifacts
echo "Removing previous build artifacts..."
rm -rf dist/ build/

# Build the package
echo "Building package..."
python -m build

# Upload the package to PyPI using Twine
echo "Uploading package to PyPI..."
twine upload dist/*

echo "Release process completed successfully."

# End of release.sh