.PHONY: setup install dev lint format typecheck test clean help

PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Create venv and install in dev mode
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e ".[dev]"
	@echo "\n\033[32mSetup complete! Activate with:\033[0m source $(VENV)/bin/activate"

install: ## Install in current environment
	pip install -e .

dev: ## Install with dev dependencies
	pip install -e ".[dev]"

lint: ## Run linter (ruff)
	$(BIN)/ruff check docs2md/

format: ## Auto-format code (ruff)
	$(BIN)/ruff format docs2md/
	$(BIN)/ruff check --fix docs2md/

typecheck: ## Run type checker (mypy)
	$(BIN)/mypy docs2md/

test: ## Run tests
	$(BIN)/pytest

clean: ## Remove venv, caches, build artifacts
	rm -rf $(VENV)
	rm -rf dist/ build/ *.egg-info
	rm -rf .mypy_cache .ruff_cache .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned!"

