.PHONY: venv deps db clean dev core clean-db clean-core clean-all migrate-new migrate-all migrate-downgrade

# Detect the operating system
UNAME_S := $(shell uname -s)

venv:
ifeq ($(OS),Windows_NT)
	pip install virtualenv
	python -m virtualenv .venv
	.venv\Scripts\activate
else
	pip install virtualenv
	python3 -m virtualenv .venv
	.venv/bin/activate
endif

deps: venv

	pip install -r requirements.txt
	pip install -r requirements-dev.txt


db: 
	docker run -d --name dev_xlock_db -e POSTGRES_USER=dev_user -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=dev_xlock -p 5432:5432 postgres:16.3-alpine3.20
	docker run -d --name dev_xlock_redis -p 6379:6379 redis:7.2.5-alpine

core:
	docker build -t xlock-core -f ./Dockerfile .
	docker run -p 8000:8000 -p 8888:8888 --name xlock-core --link dev_xlock_db:database --link dev_xlock_redis:redis -d xlock-core

clean-db:
	docker stop dev_xlock_db
	docker rm dev_xlock_db
	docker stop dev_xlock_redis
	docker rm dev_xlock_redis

clean-core:
	docker stop xlock-core
	docker rm xlock-core

clean-all: 
	$(MAKE) clean-db
	$(MAKE) clean-core

migrate-new:
	@echo "Enter migration message: "; \
	read message; \
	alembic revision -m "$$message"

migrate-all:
	PYTHONPATH=./ alembic upgrade head

migrate-downgrade:
	PYTHONPATH=./ alembic downgrade -1

dev: deps db
ifeq ($(OS),Windows_NT)
	uvicorn app.main:app --reload
else
	uvicorn app.main:app --reload
endif
