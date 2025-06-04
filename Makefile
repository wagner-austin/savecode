# Makefile ───────────────────────────────────────────────────────────
# Usage:     make <target> [VAR=value]
# Example:   make run ARGS="--git --ext js"
# -------------------------------------------------------------------

# ───────── configurable knobs (override on CLI or via env) ─────────
ifeq ($(OS),Windows_NT)
    PYTHON = py
else
    PYTHON ?= python3          # rely on whatever python is on PATH
endif
EXTS   ?= py toml ini sh ps1 html css js
RUN_DIR ?= .

# default goal
.DEFAULT_GOAL := help

# -------------------------------------------------------------------
# Targets
# -------------------------------------------------------------------
.PHONY: help install test lint build clean run \
        git git-staged git-unstaged release

help:               ## Show this help message
	@echo "---------------------------------------------------------------------"
	@echo "Savecode Makefile - Available commands:"
	@echo "---------------------------------------------------------------------"
	@echo "  help          Show this help message."
	@echo "  install       pip-install the project in editable mode + dev deps."
	@echo "  test          Run the test-suite."
	@echo "  lint          Run Ruff, Black, and MyPy."
	@echo "  build         Build sdist + wheel."
	@echo "  clean         Remove build artefacts and caches."
	@echo "  run           Run savecode on $(RUN_DIR) with $(EXTS)."
	@echo "  release       Build and upload to PyPI via Twine."
	@echo "---------------------------------------------------------------------"

install:            ## Install this package in editable mode + dev deps
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e .[dev]

test:               ## Run the test-suite
	$(PYTHON) -m pytest

lint:               ## Ruff → Black → MyPy (stop on first failure)
	ruff check --fix
	ruff format
	black .
	mypy --strict .

build:              ## Build sdist + wheel
	$(PYTHON) -m build

# ─── Cross-platform “rm -rf” helper ─────────────────────────────────
define rmdir
$(PYTHON) -c "import os, glob, shutil, sys; \
    [shutil.rmtree(p, ignore_errors=True)                         \
     for pat in sys.argv[1:]                                      \
     for p   in glob.glob(pat)                                    \
     if os.path.isdir(p)]" $(1)
endef

clean:              ## Remove build artefacts & caches
	$(call rmdir,dist build *.egg-info .pytest_cache)

run:                ## Run savecode on $(RUN_DIR) with $(EXTS)
	$(PYTHON) -m savecode $(RUN_DIR) --ext $(EXTS) $(ARGS)

git:                ## Gather all modified/untracked files
	$(PYTHON) -m savecode $(RUN_DIR) --git --all-ext $(ARGS)

git-staged:         ## Gather only files that are *staged* for commit
	$(PYTHON) -m savecode $(RUN_DIR) --git --staged --all-ext $(ARGS)

git-unstaged:       ## Gather only *unstaged* or untracked files
	$(PYTHON) -m savecode $(RUN_DIR) --git --unstaged --all-ext $(ARGS)

release: build      ## Build and upload to PyPI via Twine
	$(PYTHON) -m twine upload dist/*
