from django.urls import path

from .views import add_note, edit_note, home, note_detail

urlpatterns = [
    path("", view=home, name="home"),
    path("add/", view=add_note, name="add_note"),
    path("note/<int:note_id>/", note_detail, name="note_detail"),
    path("note/<int:note_id>/edit/", edit_note, name="edit_note"),
]
