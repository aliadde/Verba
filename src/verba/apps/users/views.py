from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import LoginForm


class UserLoginView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


@require_http_methods(["GET"])
def profile(request):
    context = {"username": "sample username", "email": "sample email", "cards": 12}
    return render(request, "profile.html", context=context)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        pass
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")
