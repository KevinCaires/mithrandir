migrate:
	docker-compose run mithrandir python manage.py makemigrations
	docker-compose run mithrandir python manage.py migrate


mithrandir:
	docker-compose exec mithrandir sh


install:
	docker-compose


build:
	docker-compose build


up:
	docker-compose up
