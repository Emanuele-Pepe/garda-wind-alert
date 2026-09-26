.PHONY: install test lint format check run help

install:  ## Install dependencies
	uv sync

test:  ## Run tests (optional filter: make test K=360)
	uv run pytest -q $(if $(K),-k "$(K)")

lint:  ## Lint with ruff
	uv run ruff check .

format:  ## Format code and apply autofixes
	uv run ruff format .
	uv run ruff check . --fix

check:  ## Everything CI runs: use before every push
	uv run ruff check .
	uv run ruff format --check .
	uv run pytest -q

run:  ## Run the alert without sending email
	uv run garda-wind-alert --dry-run

commit:  ## Guided conventional commit
	uv run cz commit

help:  ## List available commands
	@grep -E '^[a-z]+:.*## ' Makefile | awk -F':.*## ' '{printf "  %-10s %s\n", $$1, $$2}'