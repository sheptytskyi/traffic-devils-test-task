run:
	docker compose up

build:
	docker compose build

MIGRATION_NAME := initial

migrations:
	docker compose run traffic_devils alembic revision --autogenerate -m "$(MIGRATION_NAME)"

migrate:
	docker compose run traffic_devils alembic upgrade head
