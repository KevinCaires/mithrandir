migrate:
	docker-compose run mithrandir python manage.py makemigrations
	docker-compose run mithrandir python manage.py migrate


install:
	docker-compose build


shell:
	python manage.py shell


build:
	docker-compose build


up:
	docker-compose up
