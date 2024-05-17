run_dev:
	docker compose up -d
stop_dev:
	docke compose down
test:
	poetry run black ./src
	poetry run mypy ./src
	poetry run coverage run -m pytest .
	poetry run coverage html
	poetry run ruff check --fix .
	poetry sqlfluff check .\docs\sql\* --dialect postgres
#migrations:
#	alembic init migrations
#	alembic init -t async migrations
#	alembic revision --autogenerate -m "make migrations"
#	alembic upgrade heads