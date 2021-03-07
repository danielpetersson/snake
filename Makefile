.DEFAULT_GOAL: all

.PHONY: all
all: build run

.PHONY: build
build:
	poetry update
	poetry install
	./write_requirements.sh

.PHONY: run
run: build
	poetry run python server.py

.PHONY: deploy
deploy: build
	$(shell git push heroku HEAD:refs/heads/main)
