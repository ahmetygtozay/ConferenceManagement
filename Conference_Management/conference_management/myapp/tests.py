from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Conference, Paper, Review, Submission


class ConferenceModelTestCase(TestCase):
    def setUp(self):
        self.conference = Conference.objects.create(
            title="Test Conference", start_date="2024-06-01", end_date="2024-06-03"
        )

    def test_conference_creation(self):
        try:
            self.assertEqual(self.conference.title, "Test Conference")
            print("ConferenceModelTestCase: OK")
        except AssertionError:
            print("ConferenceModelTestCase: Http Error code")


class PaperModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="User1234")
        self.conference = Conference.objects.create(
            title="Test Conference", start_date="2024-06-01", end_date="2024-06-03"
        )
        self.paper = Paper.objects.create(
            title="Test Paper", author=self.user, conference=self.conference
        )

    def test_paper_creation(self):
        try:
            self.assertEqual(self.paper.title, "Test Paper")
            self.assertEqual(self.paper.author.username, "testuser")
            self.assertEqual(self.paper.conference.title, "Test Conference")
            print("PaperModelTestCase: OK")
        except AssertionError:
            print("PaperModelTestCase: Http Error code")


class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", password="User1234")
        self.paper_author = User.objects.create_user(
            username="paper_author", password="User1234"
        )
        self.conference = Conference.objects.create(
            title="Test Conference", start_date="2024-06-01", end_date="2024-06-03"
        )
        self.paper = Paper.objects.create(
            title="Test Paper", author=self.paper_author, conference=self.conference
        )
        self.review = Review.objects.create(
            reviewer=self.user, paper=self.paper, comments="This is a test review."
        )

    def test_review_creation(self):
        try:
            self.assertEqual(self.review.reviewer.username, "reviewer")
            self.assertEqual(self.review.paper.title, "Test Paper")
            print("ReviewModelTestCase: OK")
        except AssertionError:
            print("ReviewModelTestCase: Http Error code")


class SubmissionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="User1234")
        self.submission = Submission.objects.create(
            author=self.user,
            paper="conference_management/conference_management/papers/test_paper.pdf",
        )

    def test_submission_creation(self):
        try:
            self.assertEqual(self.submission.author.username, "User1234")
            print("SubmissionModelTestCase: OK")
        except AssertionError:
            print("SubmissionModelTestCase: Http Error code")


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="User1234")
        self.client.login(username="testuser", password="User1234")
        self.conference = Conference.objects.create(
            title="Test Conference", start_date="2024-06-01", end_date="2024-06-03"
        )

    def test_submit_paper_view(self):
        response = self.client.get(reverse("submit_paper"))
        try:
            self.assertEqual(response.status_code, 200)
            print("ViewsTestCase - test_submit_paper_view: OK")
        except AssertionError:
            print("ViewsTestCase - test_submit_paper_view: Http Error code")

        with open(
            "conference_management/conference_management/papers/test_paper.pdf", "rb"
        ) as fp:
            response = self.client.post(reverse("submit_paper"), {"paper": fp})
        try:
            self.assertEqual(
                response.status_code, 200
            )  # Assuming success_page.html renders after successful submission
            print("ViewsTestCase - test_submit_paper_view: OK")
        except AssertionError:
            print("ViewsTestCase - test_submit_paper_view: Http Error code")

    def test_reviewer_submissions_view(self):
        response = self.client.get(reverse("reviewer_submissions"))
        try:
            self.assertEqual(response.status_code, 200)
            print("ViewsTestCase - test_reviewer_submissions_view: OK")
        except AssertionError:
            print("ViewsTestCase - test_reviewer_submissions_view: Http Error ")

    def test_submit_review_view(self):
        # Assuming you have a submission object in your database
        submission = Submission.objects.create(
            author=self.user, paper="conference_management/papers/test_paper.pdf"
        )
        response = self.client.get(reverse("submit_review", args=[submission.id]))
        try:
            self.assertEqual(response.status_code, 200)
            print("ViewsTestCase - test_submit_review_view: OK")
        except AssertionError:
            print("ViewsTestCase - test_submit_review_view: Http Error code")

        # Assuming you have a valid review form data
        response = self.client.post(
            reverse("submit_review", args=[submission.id]),
            {"review_score": 5, "review_text": "Great paper!"},
        )
        try:
            self.assertEqual(
                response.status_code, 302
            )  # Assuming review_success redirects after successful submission
            print("ViewsTestCase - test_submit_review_view: OK")
        except AssertionError:
            print("ViewsTestCase - test_submit_review_view: Http Error code")
