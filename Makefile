# Makefile ────────────────────────────────────────────────────────────
# Usage:      make <target> [VAR=value]
# Example:    make run ARGS="--git --ext js"
# --------------------------------------------------------------------

.PHONY: help venv install test lint build clean run git git-staged git-unstaged release

# --------------------------------------------------------------------
# Configurable knobs (override on the CLI or define in an .env file)
# --------------------------------------------------------------------
PYTHON ?= python
ENV_DIR ?= .venv
EXTS   ?= py toml ini sh ps1 html css js ini
RUN_DIR ?= .

# Choose the right paths for the venv executables on any OS
ifeq ($(OS),Windows_NT)
    VENV_PY  := $(ENV_DIR)/Scripts/python.exe
    VENV_PIP := $(ENV_DIR)/Scripts/pip.exe
else
    VENV_PY  := $(ENV_DIR)/bin/python
    VENV_PIP := $(ENV_DIR)/bin/pip
endif

# Default goal -------------------------------------------------------
.DEFAULT_GOAL := help

# --------------------------------------------------------------------
# Helper: build venv only when .venv/pyvenv.cfg is absent
# --------------------------------------------------------------------
$(ENV_DIR)/pyvenv.cfg:
	$(PYTHON) -m venv $(ENV_DIR)
	$(VENV_PY) -m pip install -U pip
	$(VENV_PIP) install -e .[dev]

# --------------------------------------------------------------------
# Targets
# --------------------------------------------------------------------
help:              ## Show this help message
	@echo "---------------------------------------------------------------------"
	@echo "Savecode Makefile - Available commands:"
	@echo "---------------------------------------------------------------------"
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help                  Show this help message."
	@echo "  venv                  Create / refresh local virtual-env (part of install)."
	@echo "  install               Install project in editable mode + dev deps."
	@echo "  test                  Run the test-suite (ensures venv and deps are installed)."
	@echo "  lint                  Run linters (ruff, black, mypy)."
	@echo "  build                 Build sdist + wheel."
	@echo "  clean                 Remove build artefacts, .pytest_cache, and .venv."
	@echo "  run                   Run the savecode application (e.g., make run ARGS='--output custom.txt')."
	@echo "  release               (Placeholder - typically involves tagging, building, and uploading)."
	@echo "---------------------------------------------------------------------"

venv:              ## Create / refresh local virtual-env
	$(PYTHON) -m venv $(ENV_DIR)
	$(VENV_PY) -m pip install -U pip

install: venv      ## Install this package in editable mode + dev deps
	$(VENV_PIP) install -e .[dev]

test: $(ENV_DIR)/pyvenv.cfg  ## Run the test-suite
	$(VENV_PY) -m pytest

lint:              ## Ruff -> Black -> MyPy (stop on first failure)
	ruff check --fix
	ruff format
	black .
	mypy --strict .

build:             ## Build sdist + wheel
	$(PYTHON) -m build

# Python rm -rf macro for cross-platform directory removal
define rmdir
$(PYTHON) -c "import shutil, os, glob; [shutil.rmtree(d, ignore_errors=True) for d in glob.glob('$(1)') if os.path.isdir(d)]"
endef

clean:             ## Remove build artefacts
	$(call rmdir,dist)
	$(call rmdir,.venv)
	$(call rmdir,build)
	$(call rmdir,*.egg-info)
	$(call rmdir,.pytest_cache)

run:               ## Run savecode on $(RUN_DIR) with $(EXTS)
	$(PYTHON) -m savecode $(RUN_DIR) --ext $(EXTS) $(ARGS)

git:               ## Gather all modified/untracked files
	$(PYTHON) -m savecode $(RUN_DIR) --git --all-ext $(ARGS)

git-staged:        ## Gather only files that are *staged* for commit
	$(PYTHON) -m savecode $(RUN_DIR) --git --staged --all-ext $(ARGS)

git-unstaged:      ## Gather only *unstaged* or untracked files
	$(PYTHON) -m savecode $(RUN_DIR) --git --unstaged --all-ext $(ARGS)

release: build    ## Build and upload to PyPI via Twine
	$(PYTHON) -m twine upload dist/*
