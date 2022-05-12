#vars
APP=trails-app
USERNAME=malberti
IMAGENAME=${USERNAME}/${APP}
VERSION=latest
SERVICE=web
CONTAINERNAME=${IMAGENAME}_${SERVICE}
IMAGEFULLNAME=${CONTAINERNAME}:${VERSION}
PROJECTNAME=${USERNAME}_${APP}
PORT=5000


.PHONY: help build push all clean

help:
	@echo "Makefile commands:"
	@echo "build"
	@echo "push"
	@echo "all"

.DEFAULT_GOAL := all

build:
	docker build -t ${IMAGEFULLNAME} -f docker/web/Dockerfile .

push:
	heroku container:push web -a ${APP} --context-path . --recursive

run: 
	docker run -d --name ${CONTAINERNAME} -p 127.0.0.1:${PORT}:${PORT} -e FLASK_ENV=production -e PORT=${PORT} ${IMAGEFULLNAME}

run-it:
	docker run -it ${IMAGEFULLNAME} /entry.sh /bin/sh

run-development: 
	docker run -d --name ${CONTAINERNAME} -p 127.0.0.1:${PORT}:${PORT} -e FLASK_ENV=development -e PORT=${PORT} ${IMAGEFULLNAME}

run-development-sqlite:
	docker run -rm -d --name ${CONTAINERNAME} -p 127.0.0.1:${PORT}:${PORT} -e FLASK_TEST_DB=true -e FLASK_ENV=development -e PORT=${PORT} ${IMAGEFULLNAME} /bin/sh -c "trails --sqlite-test-db db init && python -m trails_app flask=sqlite"

stop: 
	docker stop ${CONTAINERNAME}

up:
	docker-compose -p ${PROJECTNAME} -f docker/docker-compose.yaml --project-directory . up -d

up-build:
	docker-compose -p ${PROJECTNAME} -f docker/docker-compose.yaml --project-directory . up -d --build

down:
	docker-compose -p ${PROJECTNAME} -f docker/docker-compose.yaml --project-directory . down

all: up

clean:
	docker system prune -f