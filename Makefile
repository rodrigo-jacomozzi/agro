build:
	docker-compose build

up:
	docker-compose up -d

stop:
	docker-compose stop

restart:
	docker-compose restart

migrate:
	docker-compose exec api python manage.py migrate

makemigrations:
	docker-compose exec api python manage.py makemigrations

test:
	docker-compose exec api python manage.py test -v 3
