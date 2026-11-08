from django import forms

from .models import Notes


class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["first_note", "secound_note"]
        labels = {
            "first_note": "Note",
            "secound_note": "Second note",
        }
        widgets = {
            "first_note": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Write your note...",
                    "dir": "auto",
                }
            ),
            "secound_note": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Translation, example or extra detail...",
                    "dir": "auto",
                }
            ),
        }
