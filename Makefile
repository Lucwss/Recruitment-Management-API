.PHONY: services-up services-down dev test

services-up:
	docker compose -f infra/docker/compose.yaml up -d recruitment-management-database recruitment-management-api

services-down:
	docker compose -f infra/docker/compose.yaml down

dev: services-up
	poetry run uvicorn entrypoint:app --host 0.0.0.0 --port 8000

test: services-up
	@poetry run python infra/scripts/wait_for_services.py
	poetry run pytest -vv
	$(MAKE) services-down

lint:
	pylint --rcfile=.pylintrc adapters application domain infra tests web

format:
	@echo "🔧 Running isort (imports)..."
	poetry run isort .
	@echo "🎨 Running black (code formatting)..."
	poetry run black .