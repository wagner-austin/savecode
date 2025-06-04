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

# ─── Makefile (top section, right after the other variable block) ─────────────
VENV_PY := $(ENV_DIR)/bin/python
VENV_PIP := $(ENV_DIR)/bin/pip
ifdef OS                 # Windows sets OS=Windows_NT
    VENV_PY := $(ENV_DIR)/Scripts/python.exe
    VENV_PIP := $(ENV_DIR)/Scripts/pip.exe
endif

# Default goal -------------------------------------------------------
.DEFAULT_GOAL := help

# --------------------------------------------------------------------
# Targets
# --------------------------------------------------------------------
help:              ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

venv:              ## Create / refresh local virtual-env
	$(PYTHON) -m venv $(ENV_DIR)
	$(VENV_PY) -m pip install -U pip

install: venv      ## Install this package in editable mode + dev deps
	$(VENV_PIP) install -e .[dev]

test:              ## Run the test-suite
	$(PYTHON) -m pytest

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
