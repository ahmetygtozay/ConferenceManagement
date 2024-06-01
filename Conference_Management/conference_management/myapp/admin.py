from django.contrib import admin
from .models import UserProfile
from .models import Conference
from .models import Submission


admin.site.register(UserProfile)
admin.site.register(Conference)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("author", "paper", "assigned_reviewer")
