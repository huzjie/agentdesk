.PHONY: install test lint build run

install:
	pip install -e ".[api]"

test:
	python -m unittest discover -s tests -v

verify:
	python scripts/verify.py

build:
	docker build -t agentdesk .

run:
	agentdesk serve --host 0.0.0.0 --port 8500
