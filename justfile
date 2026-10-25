# manage.py ...
manage *args:
    uv run python manage.py {{args}}

# pre-commit runner
pre-commit *args:
	uv run pre-commit {{args}}

# runserver
runserver:
	uv run python manage.py runserver
