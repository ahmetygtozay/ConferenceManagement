from django.shortcuts import render
from .models import UserProfile

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


# views.py

from django.shortcuts import render, redirect
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Kayıt başarılıysa giriş sayfasına yönlendir
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")  # Ana sayfaya yönlendir
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


from django.shortcuts import render
from .models import Conference


def conference_list(request):
    conferences = Conference.objects.all()
    return render(request, "conference_list.html", {"conferences": conferences})


def home(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect("home")


from django.shortcuts import render
from .forms import PaperSubmissionForm


# def submit_paper(request):
#     if request.method == "POST":
#         form = PaperSubmissionForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Form geçerliyse, dosyayı işleyebilirsiniz
#             paper = request.FILES["paper"]
#             # Burada dosyayı kaydetme veya işleme işlemleri yapılabilir
#             return render(request, "success_page.html")
#     else:
#         form = PaperSubmissionForm()
#     return render(request, "paper_submission.html", {"form": form})


from django.shortcuts import render, get_object_or_404
from myapp.models import Conference


def conference_detail(request, pk):
    conference = get_object_or_404(Conference, pk=pk)
    return render(request, "conference_detail.html", {"conference": conference})


from django.shortcuts import render, redirect
from .forms import PaperSubmissionForm
from .models import Submission
import random
from django.contrib.auth.models import User


def submit_paper(request):
    if request.method == "POST":
        form = PaperSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            # Formdan gelen verileri al
            author = request.user
            paper = request.FILES["paper"]

            # Submission oluştur
            submission = Submission.objects.create(author=author, paper=paper)

            # Rastgele bir reviewer seç ve submission'a ata
            reviewers = User.objects.filter(userprofile__role="Reviewer")
            if reviewers.exists():
                reviewer = random.choice(reviewers)
                submission.assigned_reviewer = reviewer
                submission.save()

            return render(request, "success_page.html")
    else:
        form = PaperSubmissionForm()
    return render(request, "paper_submission.html", {"form": form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Submission


@login_required
def reviewer_submissions(request):
    submissions = Submission.objects.filter(assigned_reviewer=request.user)
    return render(request, "reviewer_submissions.html", {"submissions": submissions})


from .models import Submission, Review
from .forms import ReviewForm


def submit_review(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_score = form.cleaned_data["review_score"]
            review_text = form.cleaned_data["review_text"]

            review = Review.objects.create(
                reviewer=request.user,
                paper=submission.paper,
                comments=review_text,
            )

            return redirect("review_success")
    else:
        form = ReviewForm()
    return render(
        request, "submit_review.html", {"form": form, "submission": submission}
    )


def review_success(request):
    return render(request, "review_success.html")


def success_page(request):
    return render(request, "success_page.html")
