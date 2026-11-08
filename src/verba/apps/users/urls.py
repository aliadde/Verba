from django.urls import path

from .views import UserLoginView, UserRegisterView, edit_profile, logout, profile

urlpatterns = [
    path("", view=profile, name="profile"),
    path("login/", view=UserLoginView.as_view(), name="login"),
    path("register/", view=UserRegisterView.as_view(), name="register"),
    path("edit_profile/", view=edit_profile, name="edit_profile"),
    path("logout/", view=logout, name="logout"),
]
