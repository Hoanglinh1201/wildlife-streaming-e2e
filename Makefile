.PHONY: build start stop restart restart-build logs

## build: rebuild the Docker images
build:
	docker compose build --no-cache

## start: start the Docker containers
start:
	docker compose up -d

## stop: stop the Docker containers
stop:
	docker compose down

## restart: restart the Docker containers
restart: stop start

## restart-build: rebuild the Docker images and restart the containers
restart-build : stop build start

logs:
	docker compose logs -f
