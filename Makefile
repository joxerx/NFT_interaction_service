.PHONY: test

init: init-envs pre-commit
init-envs:
	cp .env.example .env
	cp config.example.yaml config.yaml

pre-commit:
	pip install pre-commit --upgrade
	pre-commit install

full-migrate: makemigrations migrate
makemigrations:
	sudo docker compose exec web python ./nftProject/manage.py makemigrations
migrate:
	sudo docker compose exec web python ./nftProject/manage.py migrate

build:
	sudo docker compose up --build -d