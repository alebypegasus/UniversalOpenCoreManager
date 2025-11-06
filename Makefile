.PHONY: help setup install test lint format build clean

help:
	@echo "UOCM - Universal OpenCore Manager"
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  make setup       - Configura ambiente de desenvolvimento"
	@echo "  make install     - Instala dependências"
	@echo "  make test        - Executa testes"
	@echo "  make lint        - Verifica código com ruff"
	@echo "  make format      - Formata código com black"
	@echo "  make build       - Constrói aplicação .app"
	@echo "  make clean       - Limpa arquivos de build"

setup:
	@bash scripts/setup.sh --dev

install:
	@pip install -r requirements.txt
	@pip install -e ".[dev]"

test:
	@pytest tests/ -v

lint:
	@ruff check uocm/
	@mypy uocm/ || true

format:
	@black uocm/ tests/
	@ruff check --fix uocm/ tests/

build:
	@bash scripts/build_mac.sh

clean:
	@rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache
	@find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete

