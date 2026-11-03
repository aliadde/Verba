from django.urls import path

from .views import profile

urlpatterns = [path("", view=profile, name="profile")]
