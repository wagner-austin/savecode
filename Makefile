# Makefile ────────────────────────────────────────────────────────────
# Usage:      make <target> [VAR=value]
# Example:    make run ARGS="--git --ext js"
# --------------------------------------------------------------------

.PHONY: help venv install test lint build clean run git-run

# --------------------------------------------------------------------
# Configurable knobs (override on the CLI or define in an .env file)
# --------------------------------------------------------------------
PYTHON ?= python
ENV_DIR ?= .venv
EXTS   ?= py toml ini js
RUN_DIR ?= .

# Command that removes paths cross-platform
define rmdir
	$(PYTHON) - <<PY
import shutil, sys, pathlib, os
for p in sys.argv[1:]:
    path = pathlib.Path(p)
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
PY
endef

# Default goal -------------------------------------------------------
.DEFAULT_GOAL := help

# --------------------------------------------------------------------
# Targets
# --------------------------------------------------------------------
help:              ## Show this help
	@powershell -Command "Get-Content Makefile | ForEach-Object { if ($$_ -match '^([a-zA-Z_-]+):.*?## (.*)$$') { Write-Host -ForegroundColor Cyan ('{0,-16}' -f $$Matches[1]) -NoNewline; Write-Host $$Matches[2] } }"

venv:              ## Create / refresh local virtual-env
	$(PYTHON) -m venv $(ENV_DIR)
	$(ENV_DIR)/bin/pip install -U pip

install: venv      ## Install this package in editable mode + dev deps
	$(ENV_DIR)/bin/pip install -e .[dev]

test:              ## Run the test-suite
	$(PYTHON) -m pytest

lint:              ## Ruff -> Black -> MyPy (stop on first failure)
	ruff check --fix
	ruff format
	black .
	mypy --strict .

build:             ## Build sdist + wheel
	$(PYTHON) -m build

clean:             ## Remove build artefacts
	@$(call rmdir,dist build .pytest_cache)
	@$(call rmdir,$(shell ls -d *.egg-info 2>/dev/null || true))

run:               ## Run savecode on $(RUN_DIR) with $(EXTS)
	$(PYTHON) -m savecode $(RUN_DIR) --ext $(EXTS) $(ARGS)

git-run:           ## Same, but gather only files reported by git status
	$(PYTHON) -m savecode $(RUN_DIR) --git --ext $(EXTS) $(ARGS)
