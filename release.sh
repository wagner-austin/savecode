#!/bin/bash
# release.sh - Release automation script for the savecode package.
# This script removes previous build artifacts, rebuilds the package,
# and uploads the new version to PyPI using Twine.
# update the version number in pyproject.toml and run this script to release the package to PyPI
#run using "bash release.sh"

# use: "python -m savecode.cli -r ." for testing of changes

set -e

# Extract the version from pyproject.toml
VERSION=$(grep -Pom1 '^\s*version\s*=\s*"\K[^"]+' pyproject.toml)
echo "Using version: $VERSION"

# Remove previous build artifacts
echo "Removing previous build artifacts..."
rm -rf dist build *.egg-info || true

# Build the package
echo "Building package..."
python -m build

# Upload the package to PyPI using Twine
echo "Uploading package to PyPI..."
twine upload dist/*

echo "Release process completed successfully."

# End of release.sh