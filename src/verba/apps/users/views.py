from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def profile(request):
    context = {"username": "sample username", "email": "sample email", "cards": 12}
    return render(request, "profile.html", context=context)
