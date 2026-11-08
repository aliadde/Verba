from django.urls import path

from .views import add_note, home

urlpatterns = [
    path("", view=home, name="home"),
    path("add/", view=add_note, name="add_note"),
]
