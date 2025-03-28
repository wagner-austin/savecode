<# 
release.ps1 - Release automation script for the savecode package using PowerShell.
This script removes previous build artifacts, rebuilds the package,
and uploads the new version to PyPI using Twine.
It requires TWINE_USERNAME and TWINE_PASSWORD for authentication.
If these are not set as environment variables, the script attempts to load them
from a .pypirc file located in your home directory.
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

# Function to load TWINE credentials from the .pypirc file.
function Load-PyPiCredentials {
    $pypircPath = Join-Path $env:USERPROFILE ".pypirc"
    if (Test-Path $pypircPath) {
        Write-Host "Loading PyPI credentials from $pypircPath..."
        $inPypiSection = $false
        foreach ($line in Get-Content $pypircPath) {
            $trimmed = $line.Trim()
            # Skip comments.
            if ($trimmed -like ";*" -or $trimmed -like "#*") {
                continue
            }
            # Check for the [pypi] section.
            if ($trimmed -match "^\[pypi\]") {
                $inPypiSection = $true
                continue
            }
            # If a new section starts, exit the pypi section.
            if ($inPypiSection -and $trimmed -match "^\[.*\]") {
                break
            }
            if ($inPypiSection) {
                if ($trimmed -match "^\s*username\s*=\s*(.+)$") {
                    $env:TWINE_USERNAME = $Matches[1].Trim()
                }
                if ($trimmed -match "^\s*password\s*=\s*(.+)$") {
                    $env:TWINE_PASSWORD = $Matches[1].Trim()
                }
            }
        }
    }
    else {
        Write-Host ".pypirc file not found in $env:USERPROFILE."
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

# Attempt to load credentials from .pypirc if environment variables are not set.
if (-not $env:TWINE_USERNAME -or -not $env:TWINE_PASSWORD) {
    Load-PyPiCredentials
}

# Ensure TWINE credentials are set in the environment.
if (-not $env:TWINE_USERNAME) {
    Write-Error "TWINE_USERNAME is not set. Please set it (typically to '__token__') or configure your .pypirc file."
    exit 1
}
if (-not $env:TWINE_PASSWORD) {
    Write-Error "TWINE_PASSWORD is not set. Please set it to your PyPI API token or configure your .pypirc file."
    exit 1
}

# Upload the package to PyPI using Twine.
Write-Host "Uploading package to PyPI..."
twine upload dist/*

Write-Host "Release process completed successfully."

# End of release.ps1