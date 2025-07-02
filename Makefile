.PHONY: build start stop restart restart-build logs smoke_test_db

# Define which services (besides db) to start
OTHER_SERVICES := backend pgadmin

## build: rebuild the Docker images
build:
	docker compose build --no-cache

## start: start the Docker containers
start-db:
	docker compose up -d --wait db

start: start-db
	start-db
	docker compose up -d $(OTHER_SERVICES)

## stop: stop the Docker containers
stop:
	docker compose down

## restart: restart the Docker containers
restart: stop start

## restart-build: rebuild the Docker images and restart the containers
restart-build: stop build start

logs:
	docker compose logs -f

smoke_test_db: start-db
	docker compose up -d backend
	docker compose exec backend \
	  python -m backend.db.db_init
	docker compose down -v
