from django.contrib import admin
from .models import Conference, PaperSubmission, Review, Submission, Reviewer

admin.site.register(Conference)
admin.site.register(PaperSubmission)
admin.site.register(Review)
admin.site.register(Submission)
admin.site.register(Reviewer)
