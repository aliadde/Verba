from django.shortcuts import render

from verba.core.auth import get_payload_from_request


def home(request):
    cookies: dict[str, any] = request.COOKIES

    if cookies.get("logged_in") == "true" and get_payload_from_request(request):
        context = {"logged_in": True, "user": request.user}
    else:
        context = {"logged_in": None}

    return render(request, "home.html", context=context)
