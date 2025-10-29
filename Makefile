.PHONY: help install test format lint clean run

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install dependencies
	pip install -r requirements.txt

test:  ## Run tests with coverage
	pytest tests/ --cov=app --cov-report=term-missing --cov-report=html

test-fast:  ## Run tests without coverage
	pytest tests/ -v

format:  ## Format code with black and isort
	black app/ tests/ main.py
	isort app/ tests/ main.py

lint:  ## Run linting checks
	black --check app/ tests/ main.py
	isort --check app/ tests/ main.py
	flake8 app/ tests/ main.py

check:  ## Run all quality checks
	@make lint
	@make test

clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete

run:  ## Run the application
	uvicorn main:app --reload --host 0.0.0.0 --port 8000
