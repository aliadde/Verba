from datetime import UTC, datetime, timedelta

import jwt
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.http import require_http_methods

from .forms import EditProfileForm, LoginForm, RegisterForm


def create_access_token(user):
    now = datetime.now(UTC)

    payload = {
        "sub": str(user.pk),
        "iat": now,
        "exp": now + timedelta(minutes=30),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm="HS256",
    )


def set_auth_cookie(response, token):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
        max_age=30 * 60,
    )

    return response


class UserLoginView(View):
    template_name = "login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            token = create_access_token(form.get_user())

            response = redirect("profile")

            response = set_auth_cookie(response, token)

            return response

        return render(
            request,
            self.template_name,
            {"form": form},
            status=400,
        )


class UserRegisterView(View):
    template_name = "register.html"

    def get(self, request):
        form = RegisterForm()

        return render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            token = create_access_token(user)

            response = redirect("profile")

            return set_auth_cookie(response, token)

        return render(
            request,
            self.template_name,
            {"form": form},
            status=400,
        )


from verba.apps.notes.models import Notes
from verba.core.decorators import jwt_required


@require_http_methods(["GET"])
@jwt_required
def profile(request):
    context = {
        "username": request.user.username,
        "email": request.user.email,
        "cards": Notes.objects.filter(user=request.user).count(),
    }

    response = render(request, "profile.html", context=context)

    response.set_cookie(
        key="logged_in",
        value="true",
        samesite="Lax",
        path="/",
        max_age=30 * 60,
    )

    return response


@require_http_methods(["GET"])
@jwt_required
def logout(request):
    response = redirect("login")

    response.delete_cookie("access_token")
    response.delete_cookie("logged_in")

    return response


@jwt_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("edit_profile")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, "edit_profile.html", {"form": form})
