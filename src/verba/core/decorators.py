from functools import wraps

from django.shortcuts import redirect

from verba.core.auth import get_payload_from_request


def jwt_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        payload = get_payload_from_request(request)

        if payload is None:
            return redirect("login")

        request.jwt_payload = payload
        return view(request, *args, **kwargs)

    return wrapper
