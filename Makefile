SHELL := /bin/bash
export TEST_MODE="1"
export GUNICORN_CMD_ARGS=--bind=0.0.0.0:8012 --workers=2 --access-logfile - --error-logfile - --log-level debug
export GOOGLE_APPLICATION_CREDENTIALS=./../secrets/service-key.json


install:
	python3 -m venv ./venv
	( \
		source ./venv/bin/activate; \
		pip install --upgrade pip; \
		pip install --upgrade -r requirements.txt; \
   	)


run:
	( \
		source ./venv/bin/activate; \
		gunicorn "./app/main/main:create_app" \
	)


test:
	( \
		source ./venv/bin/activate; \
		python3 manage.py test \
	)


