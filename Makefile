.PHONY: sync test lint format check

sync:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .

# The proving command: lint, format check and tests.
check: lint test
