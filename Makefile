migrate:
	docker-compose run python managr.py makemigrations
	docker-compose run python manage.py migrate


mithrandir:
	docker-compose exec mithrandir sh


install:
	docker-compose build


build:
	docker-compose build


up:
	docker-compose up
