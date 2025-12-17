SHELL := /bin/bash
VENV_DIR = newnews_venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

.DEFAULT_GOAL := help

.PHONY: help install run clean init-cloud nuke-db

help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Set up environment & dependencies
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@printf "\033[1;32mEnvironment ready! Don't forget to configure your .env file. 🧑‍🚀\033[0m\n"

run: ## Launch CLI interface
	$(PYTHON) main.py

clean: ## Reset workspace (remove venv and cache)
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@if [ -d $(VENV_DIR) ]; then rmdir $(VENV_DIR); fi
	@echo "Workspace cleaned. 🧹"

init-cloud: ## Provision the DynamoDB table and S3 Bucket
	@printf "\033[32mSummoning Cloud Resources... 🔮\033[0m\n"
	$(PYTHON) -m src.db_ops --action init
	@printf "\033[32mInfrastructure ready.\033[0m\n"

nuke-db: ## Destroy records from DynamoDB and S3 Bucket
	@printf "\033[31mWARNING: This will incinerate all data in the table.\033[0m\n"
	@read -p "Are you sure? [y/N]: " confirm && if [ "$$confirm" = "y" ]; then \
		$(PYTHON) -m src.db_ops --action nuke; \
	fi