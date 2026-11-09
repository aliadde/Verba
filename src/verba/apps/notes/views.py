from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.cache import never_cache

from verba.apps.users.models import Users
from verba.core.auth import get_payload_from_request
from verba.core.decorators import jwt_optional, jwt_required

from .forms import NoteForm
from .models import Notes


@never_cache
@jwt_optional
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


@jwt_required
def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note added successfully.")
            return redirect("home")
    else:
        form = NoteForm()

    return render(request, "add_note.html", {"form": form})


@jwt_required
def note_detail(request, note_id):
    note = get_object_or_404(Notes, pk=note_id, user=request.user)
    return render(request, "note_detail.html", {"note": note})


@jwt_required
def edit_note(request, note_id):
    note = get_object_or_404(Notes, pk=note_id, user=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.updated_at = timezone.localdate()  # تاریخ آخرین ویرایش
            note.save()
            messages.success(request, "Note updated successfully.")
            return redirect("note_detail", note_id=note.id)
    else:
        form = NoteForm(instance=note)

    return render(request, "edit_note.html", {"form": form, "note": note})
