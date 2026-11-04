from django.urls import path

from .views import login, profile

urlpatterns = [
    path("", view=profile, name="profile"),
    path("login/", view=login, name="login"),
]
