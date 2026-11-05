from django.urls import path

from .views import UserLoginView, UserRegisterView, profile

urlpatterns = [
    path("", view=profile, name="profile"),
    path("login/", view=UserLoginView.as_view(), name="login"),
    path("register/", view=UserRegisterView.as_view(), name="register"),
]
