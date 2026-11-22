.PHONY: sync dev dev-api dev-web test lint format migrate check

WEB = npm --prefix web

# Install or update both environments after a change to pyproject.toml, uv.lock or web/package-lock.json.
sync:
	uv sync
	$(WEB) ci

# Backend on 127.0.0.1:8000 and the web app on 127.0.0.1:5173 (it proxies /api to the backend).
dev:
	$(MAKE) -j2 dev-api dev-web

dev-api:
	uv run uvicorn evidence_meter.entrypoints.api:app --host 127.0.0.1 --port 8000 --reload

dev-web:
	$(WEB) run dev

test:
	uv run pytest
	$(WEB) test

# Style, the dependency rule between contexts (tests/test_architecture.py), web lint and type check.
lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run pytest tests/test_architecture.py -q
	$(WEB) run lint
	$(WEB) run typecheck

format:
	uv run ruff format .

# Apply pending migrations to $$EVIDENCE_METER_DB (default var/evidence-meter.sqlite3).
migrate:
	uv run python -m evidence_meter.platform.migrate

# The proving command: lint, format check, the dependency rule and all tests.
check: lint test
