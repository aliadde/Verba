from django.shortcuts import render


def profile(request):
    if request.method == "GET":
        context = {"username": "sample username", "email": "sample email", "cards": 12}
        return render(request, "profile.html", context=context)
