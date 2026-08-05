APP_NAME=student-rest-api
VERSION=v1.0.2
CONTAINER_NAME=student-api

build:
	docker build -t $(APP_NAME):$(VERSION) .

run:
	-docker rm -f $(CONTAINER_NAME)
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p 5000:5000 \
		-e DATABASE_URL=sqlite:///students.db \
		$(APP_NAME):$(VERSION)

stop:
	-docker stop $(CONTAINER_NAME)

remove:
	-docker rm $(CONTAINER_NAME)

restart: stop run

logs:
	docker logs -f $(CONTAINER_NAME)

ps:
	docker ps

images:
	docker images

clean:
	-docker rm -f $(CONTAINER_NAME)
	-docker rmi $(APP_NAME):$(VERSION)
