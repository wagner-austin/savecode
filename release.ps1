<# 
release.ps1 - Release automation script for the savecode package using PowerShell.
This script removes previous build artifacts, rebuilds the package,
requires TWINE_USERNAME and TWINE_PASSWORD environment variables for PyPI authentication,
and uploads the new version to PyPI using Twine.
Make sure to set the TWINE_USERNAME and TWINE_PASSWORD environment variables before running this script.
Alternatively, create a .pypirc file in your home directory with your PyPI credentials.
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

# Ensure TWINE credentials are set in the environment.
if (-not $env:TWINE_USERNAME) {
    Write-Error "TWINE_USERNAME is not set. Please set it (typically to '__token__') before running this script."
    exit 1
}
if (-not $env:TWINE_PASSWORD) {
    Write-Error "TWINE_PASSWORD is not set. Please set it to your PyPI API token before running this script."
    exit 1
}

# Upload the package to PyPI using Twine.
Write-Host "Uploading package to PyPI..."
twine upload dist/*

Write-Host "Release process completed successfully."

# End of release.ps1