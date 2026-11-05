from datetime import UTC, datetime, timedelta

import jwt
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.http import require_http_methods

from .forms import LoginForm


class UserLoginView(View):
    template_name = "login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            now = datetime.now(UTC)

            payload = {
                "sub": str(user.pk),
                "iat": now,
                "exp": now + timedelta(minutes=30),
            }

            token = jwt.encode(
                payload,
                settings.JWT_SECRET_KEY,
                algorithm="HS256",
            )

            response = redirect("profile")

            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=30 * 60,
            )

            return response

        return render(
            request,
            self.template_name,
            {"form": form},
            status=400,
        )


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
