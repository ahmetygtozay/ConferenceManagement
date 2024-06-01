from django import forms


class PaperSubmissionForm(forms.Form):
    paper = forms.FileField(
        label="Select a file",
        help_text="Only DOCX and PDF formats are allowed.",
        widget=forms.FileInput(attrs={"accept": ".docx, .pdf"}),
    )


from django import forms


class ReviewForm(forms.Form):
    review_score = forms.IntegerField(label="Review Score", min_value=0, max_value=10)
    review_text = forms.CharField(label="Review Text", widget=forms.Textarea)


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
