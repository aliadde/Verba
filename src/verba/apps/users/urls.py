from django.urls import path

from .views import UserLoginView, profile, register

urlpatterns = [
    path("", view=profile, name="profile"),
    path("login/", view=UserLoginView.as_view(), name="login"),
    path("register/", view=register, name="register"),
]
