.PHONY: build up down logs test-backend test-frontend lint format

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

test-backend:
	docker compose exec backend pytest

test-frontend:
	docker compose exec frontend npm test

lint:
	-ruff check --config pyproject.toml backend

format:
	-ruff check --fix --config pyproject.toml backend
	ruff format --config pyproject.toml backend
