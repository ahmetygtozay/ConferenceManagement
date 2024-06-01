from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Conference(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    # Diğer konferans özelliklerini ekleyebilirsiniz


class UserProfile(models.Model):
    USER_ROLES = [
        ("Attendee", "Attendee"),
        ("Author", "Author"),
        ("Reviewer", "Reviewer"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES)


class Paper(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    submitted = models.BooleanField(default=False)
    assigned_reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_papers",
        null=True,
        blank=True,
    )


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    comments = models.TextField()


from django.db import models
from django.contrib.auth.models import User


class Submission(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submissions"
    )
    paper = models.FileField(upload_to="papers/")
    assigned_reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_submissions",
        null=True,
        blank=True,
    )
