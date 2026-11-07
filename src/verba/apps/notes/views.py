from django.shortcuts import get_object_or_404, render

from verba.apps.users.models import Users
from verba.core.auth import get_payload_from_request


def home(request):
    cookies: dict[str, any] = request.COOKIES

    if cookies.get("logged_in") == "true" and get_payload_from_request(request):
        # jwt toekn check
        payload = get_payload_from_request(request)
        user_id = payload.get("sub")
        # get user from database
        user = get_object_or_404(Users, id=user_id)

        notes = user.notes_set.all()

        context = {"logged_in": True, "user": user, "user_notes": notes}
    else:
        context = {"logged_in": None}

    return render(request, "home.html", context=context)
