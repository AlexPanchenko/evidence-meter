.PHONY: sync dev dev-api dev-web test lint format migrate diagrams check

WEB = npm --prefix web
# mermaid-cli renders with a Chromium kept in web/node_modules (see web/.puppeteerrc.cjs).
export PUPPETEER_CACHE_DIR := $(CURDIR)/web/node_modules/.cache/puppeteer
# Extra mmdc flags; CI passes a puppeteer config there.
MMDC_FLAGS ?=

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

# Render every Mermaid block in tracked Markdown with mermaid-cli; a diagram that does not parse fails.
# Not part of check: Chromium cannot start inside the agent sandbox. CI runs it.
diagrams:
	@mkdir -p var/diagrams
	@set -e; for f in $$(git grep -l '```mermaid' -- '*.md'); do \
		echo "render $$f"; \
		$(WEB) exec -- mmdc --quiet $(MMDC_FLAGS) -i "$$f" -o "var/diagrams/$$(echo $$f | tr / _)"; \
	done

# The proving command: lint, format check, the dependency rule and all tests.
check: lint test
