.PHONY: venv test lint build clean run

venv:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip

test:
	python -m pytest

lint:
	ruff check --fix
	ruff format
	black .
	mypy --strict .

build:
	python -m build

clean:
	rm -rf dist build *.egg-info .pytest_cache

run:
	python -m savecode .
