install:
	poetry install

dev:
	poetry run flask --app horssite_flask:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) horssite_flask:app

build:
	./build.sh

lint:
	poetry run flake8

collect:
	poetry build
	poetry publish --dry-run
	pip install --user --force-reinstall dist/*.whl
