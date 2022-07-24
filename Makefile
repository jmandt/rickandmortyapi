
.ONESHELL:
SHELL := /bin/bash

CONTAINER_NAME=rickandmortyapi
CONTAINER_VERSION=latest

.PHONY: build-api
build-api:
	@docker-compose -f docker-compose.yml build

.PHONY: run-api
run-api: stop-api build-api
	@docker-compose -f docker-compose.yml up

.PHONY: stop-api
stop-api:
	@docker-compose -f docker-compose.yml down


.PHONY: tests
tests:
	@export PYTHONPATH=./app
	@poetry run pytest -p no:warnings --cov=./app --cov-fail-under=95 -vv ./tests

