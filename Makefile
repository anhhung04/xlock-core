.PHONY: deps db clean dev core clean-db clean-core clean-all migrate-new migrate-all migrate-downgrade

setup_env:
	pip install virtualenv
	virtualenv .venv

deps: 
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

db: 
	docker run -d --name dev_xlock_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5432:5432 postgres:16.3-alpine3.20
	docker run -d --name dev_xlock_redis -p 6379:6379 redis:7.2.5-alpine

view-db:
	docker compose --profile dev exec postgres-dev psql postgres --username postgres -w

clean-db:
	docker stop dev_xlock_db
	docker rm dev_xlock_db
	docker stop dev_xlock_redis
	docker rm dev_xlock_redis

clean-all: 
	$(MAKE) clean-db
	$(MAKE) clean-core

migrate-new:
	@echo "Enter migration message: "; \
	read message; \
	alembic revision --autogenerate -m "$$message"

migrate-all:
	alembic upgrade head

migrate-downgrade:
	alembic downgrade -1

up-dev:
	docker compose --profile dev up -d --build

down-dev:
	docker compose --profile dev down

logs:
	docker compose --profile dev logs -f

dev: down-dev up-dev
	fastapi dev app.py --reload --host 0.0.0.0 --port 8000

restart-server:
	fastapi dev app.py --reload --host 0.0.0.0 --port 8000


