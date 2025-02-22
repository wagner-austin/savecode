# savecode

Save Python code from directories and files into one output file.

## Updating the Code and Publishing a New Release

Follow these steps to update the package on PyPI:

### 1. Update Your Code

- Make the necessary changes to your code (e.g., in `savecode/cli.py`).
- Update the version number in both:
  - `setup.py` (the `version` field)
  - `savecode/__init__.py` (the `__version__` variable)

### 2. Commit Your Changes

Use Git to commit your changes:
```bash
git add .
git commit -m "Update code and bump version to X.Y.Z"
git push
