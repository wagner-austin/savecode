<# 
release.ps1 - Release automation script for the savecode package using PowerShell.
This script removes previous build artifacts, rebuilds the package,
sets environment variables for PyPI authentication, and uploads the new version to PyPI using Twine.
Make sure to set the TWINE_USERNAME and TWINE_PASSWORD environment variables before running this script.
Make a .pypirc file in your home directory with the following content:
[pypi]
username = __token__
password = <your_token>
Run using: PowerShell -ExecutionPolicy Bypass -File release.ps1
#>

# Exit on any error.
$ErrorActionPreference = "Stop"

# Function to extract the version from savecode/__init__.py using regex.
function Get-Version {
    $initFile = "savecode/__init__.py"
    if (-Not (Test-Path $initFile)) {
        Write-Host "Error: $initFile not found."
        exit 1
    }
    $content = Get-Content $initFile -Raw
    $versionRegex = '__version__\s*=\s*["'']([^"'']+)["'']'
    if ($content -match $versionRegex) {
        return $Matches[1]
    }
    else {
        return "0.0.0"
    }
}

# Extract the version.
$VERSION = Get-Version
Write-Host "Using version: $VERSION"

# Remove previous build artifacts.
Write-Host "Removing previous build artifacts..."
$dirsToRemove = @("dist", "build")
foreach ($dir in $dirsToRemove) {
    if (Test-Path $dir) {
        Remove-Item $dir -Recurse -Force
        Write-Host "Removed $dir"
    }
}

# Build the package.
Write-Host "Building package..."
python -m build

# Optional: Set TWINE credentials via environment variables to avoid interactive prompts.
# Ensure you replace the token below with your current, valid API token if needed.
if (-not $env:TWINE_USERNAME) {
    Write-Host "TWINE_USERNAME is not set. Setting it to __token__"
    $env:TWINE_USERNAME = "__token__"
}
if (-not $env:TWINE_PASSWORD) {
    Write-Host "TWINE_PASSWORD is not set. Setting it to the provided API token."
    $env:TWINE_PASSWORD = "<your_token>"
}

# Upload the package to PyPI using Twine.
Write-Host "Uploading package to PyPI..."
twine upload dist/*

Write-Host "Release process completed successfully."

# End of release.ps1