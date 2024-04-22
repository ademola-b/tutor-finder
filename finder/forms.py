from django import forms
from accounts.models import Tutor
from . models import SessionBook

class BookSessionForm(forms.ModelForm):
    class Meta:
        model = SessionBook
        fields = [
            "subject",
            "additional_note",
            "duration",
        ]