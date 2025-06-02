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
	powershell -Command "if (Test-Path dist) { Remove-Item -Recurse -Force dist }"
	powershell -Command "if (Test-Path build) { Remove-Item -Recurse -Force build }"
	powershell -Command "Remove-Item -Recurse -Force -ErrorAction SilentlyContinue *.egg-info"
	powershell -Command "if (Test-Path .pytest_cache) { Remove-Item -Recurse -Force .pytest_cache }"

run:
	python -m savecode . --ext py toml ini js
