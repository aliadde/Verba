from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def profile(request):
    context = {"username": "sample username", "email": "sample email", "cards": 12}
    return render(request, "profile.html", context=context)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        # validate with form

        # create jwt toekn and send to browser for saving

        pass
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")
