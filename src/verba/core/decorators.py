from functools import wraps

from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils.cache import add_never_cache_headers

from verba.core.auth import get_payload_from_request

User = get_user_model()


def jwt_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        payload = get_payload_from_request(request)

        if payload is None:
            return redirect("login")

        try:
            user = User.objects.get(pk=payload["sub"])
        except (User.DoesNotExist, KeyError, ValueError):
            response = redirect("login")
            response.delete_cookie("access_token")
            response.delete_cookie("logged_in")
            return response

        request.jwt_payload = payload
        request.user = user

        response = view(request, *args, **kwargs)
        add_never_cache_headers(response)  # کش نشود
        response["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0, private"
        )
        return response

    return wrapper
