.DEFAULT_GOAL: all

.PHONY: all
all: install all

.PHONY: install
install:
	poetry install
	./write_requirements.sh

.PHONY: run
run: install
	poetry run python server.py

#.PHONY: publish
#publish: all
