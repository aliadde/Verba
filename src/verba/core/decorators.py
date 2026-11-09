from functools import wraps

from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers

from verba.core.auth import authenticate, clear_auth_cookies, set_auth_cookies


def _finish(response, new_tokens):
    if new_tokens:
        set_auth_cookies(response, *new_tokens)
    add_never_cache_headers(response)
    response["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0, private"
    )
    return response


def jwt_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        user, new_tokens = authenticate(request)
        if user is None:
            return clear_auth_cookies(redirect("login"))

        request.user = user
        return _finish(view(request, *args, **kwargs), new_tokens)

    return wrapper


def jwt_optional(view):
    """برای صفحه‌هایی مثل Home که مهمان هم می‌تواند ببیند."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        user, new_tokens = authenticate(request)
        request.user = user  # None برای مهمان
        return _finish(view(request, *args, **kwargs), new_tokens)

    return wrapper
