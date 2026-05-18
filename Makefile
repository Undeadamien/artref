SOURCES = src
TESTS = tests
TARGETS = $(SOURCES) $(TESTS)

dev:
	pip install -e ".[dev]"

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

clean:
	docker compose down -v

re: clean
	docker compose up --build -d

lint:
	@black --check -q $(TARGETS)
	@isort --check-only -q --profile black $(TARGETS)
	@pyright $(TARGETS)

format:
	@black -q --fast $(TARGETS)
	@isort -q --profile black $(TARGETS)

server:
	uvicorn artref.api.main:app --reload

test:
	@pytest --cov

test-all:
	@pytest -m '' --cov

docs:
	@xdg-open http://localhost:8000/docs

.PHONY: dev up down build clean re lint format server test test-all docs
