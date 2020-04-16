run:
	python manage.py runserver 127.0.0.1:6006


migrate:
	python manage.py makemigrations
	python manage.py migrate


shell:
	python manage.py shell


install:
	pip install -r requirements/dev.txt

