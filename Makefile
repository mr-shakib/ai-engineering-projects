.PHONY: help setup install test lint format clean

help:
	@echo "AI Engineering Projects - Available Commands"
	@echo "============================================="
	@echo "make setup      - Initial setup (create venv, install dependencies)"
	@echo "make install    - Install development dependencies"
	@echo "make test       - Run all tests"
	@echo "make lint       - Run linting and type checking"
	@echo "make format     - Format code with Black and isort"
	@echo "make clean      - Remove generated files and caches"
	@echo "make new PROJECT=name - Create new project"

setup:
	python scripts/setup.py

install:
	pip install -r requirements-dev.txt

test:
	python scripts/test_all.py

lint:
	python scripts/lint.py --check

format:
	black .
	isort .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/ .coverage

new:
	python scripts/create_project.py $(PROJECT)
