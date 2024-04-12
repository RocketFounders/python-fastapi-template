include .env
export

.PHONY: new_migration migrate uvicorn_start start_celery

new_migration:
	@read -p "Enter name: " param;migrate create -ext sql -dir ./core/storage/db/migrations -seq $$param

migrate:
	migrate -database ${DATABASE_URL} -path ./core/storage/migrations up

uvicorn_start:
	poetry run uvicorn main:app

start_celery:
	celery -A tasks.celery_app worker --loglevel=info
