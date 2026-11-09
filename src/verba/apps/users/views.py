from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_http_methods

from verba.core.auth import (
    clear_auth_cookies,
    revoke_refresh_token,
    start_session,
)
from verba.core.decorators import jwt_required

from .forms import EditProfileForm, LoginForm, RegisterForm


class UserLoginView(View):
    template_name = "login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            return start_session(redirect("profile"), form.get_user())

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
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            return start_session(redirect("profile"), user)

        return render(
            request,
            self.template_name,
            {"form": form},
            status=400,
        )


@require_http_methods(["GET"])
@jwt_required
def profile(request):
    context = {
        "username": request.user.username,
        "email": request.user.email,
        # مدل Notes فیلد user بدون related_name دارد، پس اسم پیش‌فرض این است
        "cards": request.user.notes_set.count(),
    }
    return render(request, "profile.html", context=context)


@require_http_methods(["GET"])
def logout(request):
    # عمداً بدون jwt_required: کاربری که access‌اش منقضی شده هم باید بتواند خارج شود
    raw = request.COOKIES.get("refresh_token")
    if raw:
        revoke_refresh_token(raw)  # در دیتابیس هم باطل شود

    response = clear_auth_cookies(redirect("login"))
    response["Clear-Site-Data"] = '"cache", "storage"'
    return response


@jwt_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.updated_at = timezone.now()
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("edit_profile")
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "edit_profile.html", {"form": form})
