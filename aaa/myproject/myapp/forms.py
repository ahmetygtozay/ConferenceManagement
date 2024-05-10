from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):

    pass


class LoginForm(AuthenticationForm):

    pass


from django import forms
from .models import Conference


class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = [
            "title",
            "description",
            "date",
            "location",
        ]  # Gerekli alanları burada belirtin


from django import forms


class RoleSelectionForm(forms.Form):
    ROLES = [
        ("Attendee", "Attendee"),
        ("Author", "Author"),
        ("Reviewer", "Reviewer"),
    ]
    role = forms.ChoiceField(choices=ROLES)


from django import forms
from django.core.exceptions import ValidationError


class PaperSubmissionForm(forms.Form):
    title = forms.CharField(max_length=100)
    document = forms.FileField(
        label="Select a file", help_text="Only DOCX or PDF files are allowed."
    )

    def clean_document(self):
        file = self.cleaned_data["document"]
        if not file.name.endswith((".docx", ".pdf")):
            raise ValidationError("Only DOCX or PDF files are allowed.")
        return file


from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content"]
