from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

DEBUG = True

SECRET_KEY = 'django-insecure-+%8x)@avpph675^v3se(0ick1k^^rt(1&f&y*d054#-e^advo)'

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "verba"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
