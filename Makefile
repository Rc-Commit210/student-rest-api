APP_NAME=student-rest-api
VERSION=v1.0.3
DOCKERHUB_USERNAME=rcsanket753
IMAGE=$(DOCKERHUB_USERNAME)/$(APP_NAME):$(VERSION)
COMPOSE=docker compose

.PHONY: \
	db-start \
	db-wait \
	migrate \
	build \
	api-start \
	up \
	down \
	logs \
	ps \
	clean \
	test \
	lint \
	format \
	docker-login \
	docker-push

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

test:
	$(COMPOSE) run --rm api python -m pytest -v

format:
	$(COMPOSE) run --rm api black app tests run.py

lint:
	$(COMPOSE) run --rm api flake8 app tests run.py

docker-login:
	@echo "$$DOCKERHUB_TOKEN" | docker login \
		-u "$(DOCKERHUB_USERNAME)" \
		--password-stdin

docker-push:
	docker tag $(APP_NAME):$(VERSION) $(IMAGE)
	docker push $(IMAGE)

clean:
	$(COMPOSE) down --volumes --remove-orphans
	-docker rmi $(APP_NAME):$(VERSION)
