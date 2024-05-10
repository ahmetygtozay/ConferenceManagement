from django.urls import path
from myapp.views import (
    register_view,
    login_view,
    home_view,
    logout_view,
    conferences_view,
    create_conference_view,
    register_conference_view,
    paper_submission_view,
    reviewer_dashboard,
    review_document,
    profile_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("conferences/", conferences_view, name="conferences"),
    path("create_conference/", create_conference_view, name="create_conference"),
    path(
        "conferences/<int:conference_id>/register/",
        register_conference_view,
        name="register_conference",
    ),
    path(
        "conferences/<int:conference_id>/submit_paper/",
        paper_submission_view,
        name="paper_submission",
    ),
    path("reviewer/dashboard/", reviewer_dashboard, name="reviewer_dashboard"),
    path("reviewer/review/<int:document_id>/", review_document, name="review_document"),
    path("profile/", profile_view, name="profile"),
]
