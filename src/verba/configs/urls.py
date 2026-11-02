from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def redirecter(request):
    return redirect("home")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", redirecter),
    path("/", redirecter),
    path("note/", include("verba.apps.notes.urls")),
]
