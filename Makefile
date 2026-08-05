APP_NAME=student-rest-api
VERSION=v1.0.3

COMPOSE=docker compose

.PHONY: db-start db-wait migrate build api-start up down logs ps clean

db-start:
	$(COMPOSE) up -d db

db-wait:
	@echo "Waiting for PostgreSQL..."
	@until $(COMPOSE) exec -T db pg_isready -U student -d studentdb; do \
		sleep 2; \
	done
	@echo "PostgreSQL is ready."

migrate:
	$(COMPOSE) run --rm api flask db upgrade

build:
	$(COMPOSE) build api

api-start:
	$(COMPOSE) up -d api

up: db-start db-wait build migrate api-start
	@echo "Student API and PostgreSQL are running."
	@echo "Healthcheck: http://localhost:5000/healthcheck"

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

clean:
	$(COMPOSE) down --volumes --remove-orphans
	-docker rmi $(APP_NAME):$(VERSION)
