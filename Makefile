.PHONY: build start stop restart restart-build logs smoke_test_db

# Define which services (besides db) to start

## build: rebuild the Docker images
build-no-cache:
	docker compose build --no-cache

build:
	docker compose build

start:
	docker compose up -d

start-dev:
	docker compose up

## stop: stop the Docker containers
stop:
	docker compose down

## restart: restart the Docker containers
restart: stop start

## restart-build: rebuild the Docker images and restart the containers
restart-build: stop build start
restart-build-no-cache: stop build-no-cache start

logs:
	docker compose logs -f
