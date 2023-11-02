include .env
export

new_migration:
	@read -p "Enter name: " param;migrate create -ext sql -dir ./core/storage/db/migrations -seq $$param

migrate:
	migrate -database ${DATABASE_URL} -path ./core/storage/migrations up

uvicorn_start:
	poetry run uvicorn main:app
