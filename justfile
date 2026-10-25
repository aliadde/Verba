# manage.py ...
manage *args:
    uv run python manage.py {{args}}

# pre-commit runner
pre-commit *args:
	uv run pre-commit {{args}}

# runserver
runserver:
	uv run python manage.py runserver

# migrate
migrate:
	uv run python manage.py migrate

# makemigration
makemigration:
	uv run python manage.py makemigrations
