.PHONY: routes server

THIS_ENV = . env/bin/activate
PYTHON = env/bin/python
COVERAGE = env/bin/coverage
RUFF = env/bin/ruff

env:
	python3.12 -m venv env
	env/bin/pip install -r requirements.txt
	mkdir temp

routes:
	$(PYTHON) -m flask --app server routes

server:
	$(PYTHON) server.py

db-regen:
	sh ./bin/db-start.sh