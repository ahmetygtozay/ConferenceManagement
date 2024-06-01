from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from myapp.views import (
    logout_view,
    submit_paper,
    conference_detail,
    reviewer_submissions,
    submit_review,
    review_success,
    success_page,
)

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("conferences/", views.conference_list, name="conference_list"),
    path("logout/", logout_view, name="logout"),
    path("submit_paper/", submit_paper, name="submit_paper"),
    path("conference/<int:pk>/", conference_detail, name="conference_detail"),
    path("reviewer_submissions/", reviewer_submissions, name="reviewer_submissions"),
    path("submit_review/<int:submission_id>/", submit_review, name="submit_review"),
    path("review_success/", review_success, name="review_success"),
    path("success_page/", success_page, name="success_page"),
    # Diğer URL yönlendirmeleri
]
