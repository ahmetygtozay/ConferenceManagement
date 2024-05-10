from django.db import models
from django.contrib.auth.models import User


class Conference(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    attendees = models.ManyToManyField(User, related_name="attended_conferences")

    def __str__(self):
        return self.title


from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/")
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_documents",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authored_documents",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Review of {self.document.title} by {self.reviewer.username}"


from django.contrib.auth.models import User
from django.db import models
from .models import Conference


class Submission(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submission_as_author"
    )
    file = models.FileField(upload_to="submissions/")
    assigned_reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submission_as_reviewer"
    )
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)


class PaperSubmission(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="paper_submission_as_author"
    )
    file = models.FileField(upload_to="papers/")
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)


from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @property
    def submitted_papers(self):
        return self.user.authored_documents.count()

    @property
    def registered_conferences(self):
        return self.user.attended_conferences.count()

    @property
    def reviewed_papers(self):
        return self.user.reviewed_documents.count()


from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "content"
        ]  # İnceleme içeriği haricinde başka alanlar varsa buraya ekleyin

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["document"] = forms.ModelChoiceField(
            queryset=Document.objects.all()
        )  # Burada belge alanını ekliyoruz


from django.db import models


class Reviewer(models.Model):
    reviewer_id = models.AutoField(primary_key=True)
    reviewer_name = models.CharField(max_length=100)
    # Diğer alanları ekleyebilirsiniz, örneğin email, kurum bilgisi, vs.

    def __str__(self):
        return self.reviewer_name


# models.py

from django.db import models
from django.contrib.auth.models import User
from .models import Document


class Assigned(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        User, related_name="assigned_documents", on_delete=models.CASCADE
    )
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document.title} assigned to {self.reviewer.username} on {self.assigned_date}"
