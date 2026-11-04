from django.urls import path

from .views import login, profile, register

urlpatterns = [
    path("", view=profile, name="profile"),
    path("login/", view=login, name="login"),
    path("register/", view=register, name="register"),
]
