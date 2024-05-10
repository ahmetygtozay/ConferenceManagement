from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render
from .models import Conference
from .forms import ConferenceForm, ReviewForm
from .models import Document, Review


def home_view(request):
    return render(request, "home.html")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(
                "home"
            )  # Burada 'home' yerine giriş yaptıktan sonra yönlendirilmek istediğiniz URL'yi belirtin
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(
                    "home"
                )  # Burada 'home' yerine giriş yaptıktan sonra yönlendirilmek istediğiniz URL'yi belirtin
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


from django.shortcuts import render, redirect
from .models import Conference
from .forms import ConferenceForm


def create_conference_view(request):
    if request.method == "POST":
        form = ConferenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "conferences"
            )  # Konferans oluşturulduktan sonra conferences_view'e yönlendir
    else:
        form = ConferenceForm()
    return render(request, "create_conference.html", {"form": form})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Conference
from .forms import RoleSelectionForm, PaperSubmissionForm


def conferences_view(request):
    conferences = Conference.objects.all()
    return render(request, "conferences.html", {"conferences": conferences})


def register_conference_view(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == "POST":
        form = RoleSelectionForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data["role"]
            if role == "Attendee":
                messages.success(request, "Kaydınız tamamlandı.")
            elif role == "Author":
                return redirect("paper_submission", conference_id=conference.id)
            elif role == "Reviewer":
                assign_document_to_reviewer(request, conference)
                return redirect("reviewer_dashboard")
    else:
        form = RoleSelectionForm()
    return render(
        request, "register_conference.html", {"form": form, "conference": conference}
    )


from .forms import PaperSubmissionForm
from .models import Conference, PaperSubmission


def paper_submission_view(request, conference_id):
    conference = Conference.objects.get(id=conference_id)
    if request.method == "POST":
        form = PaperSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            if "file" in request.FILES:
                submission = PaperSubmission(
                    conference=conference,
                    author=request.user,
                    file=request.FILES["file"],
                )
                submission.save()

                messages.success(request, "Belgeniz başarıyla gönderildi.")
                return redirect("home")
            else:
                messages.error(request, "Dosya yüklenirken bir hata oluştu.")
    else:
        form = PaperSubmissionForm()
    return render(
        request, "paper_submission.html", {"form": form, "conference": conference}
    )


from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404
from .models import Conference


from .models import Document


from .models import Reviewer


def assign_reviewer_to_paper(paper):
    # Burada bir reviewer ataması yapılacak
    # Örneğin, rastgele bir hakem seçilebilir veya belirli kriterlere göre bir hakem atanabilir

    # Örnek olarak, rastgele bir hakemi seçelim
    random_reviewer = Reviewer.objects.order_by("?").first()

    # Atama yapılacaksa
    if random_reviewer:
        paper.reviewer = random_reviewer
        paper.save()


def get_document_to_assign(conference_id):
    # Atanmamış bir belgeyi al
    # Bu, örneğin, henüz atanmamış ilk belgeyi getiren bir sorgu olabilir
    return Document.objects.filter(
        conference_id=conference_id, reviewer__isnull=True
    ).first()


def review_document_view(request, document_id):
    document = Document.objects.get(id=document_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.document = document  # Document alanını form üzerinden atıyoruz
            review.reviewer = request.user
            review.save()
            messages.success(request, "Belge başarıyla incelendi.")
            return redirect("home")
    else:
        form = ReviewForm()
    return render(request, "review_document.html", {"form": form, "document": document})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Document, Review


def reviewer_dashboard(request):
    assigned_documents = Document.objects.filter(reviewer=request.user)
    return render(
        request, "reviewer_dashboard.html", {"assigned_documents": assigned_documents}
    )


def review_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.document = document
            review.reviewer = request.user
            review.save()
            return redirect("reviewer_dashboard")
    else:
        form = ReviewForm()
    return render(request, "review_document.html", {"form": form, "document": document})


from django.shortcuts import render
from .models import Document, Conference
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from .models import PaperSubmission, Review
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    user = request.user
    submitted_documents = PaperSubmission.objects.filter(author=user)
    reviewed_documents = Review.objects.filter(reviewer=user)

    context = {
        "submitted_documents": submitted_documents,
        "reviewed_documents": reviewed_documents,
    }
    return render(request, "profile.html", context)


def submission_list(request):
    submissions = Submission.objects.all()
    return render(request, "submission_list.html", {"submissions": submissions})


# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Conference, Assigned
from .forms import RoleSelectionForm, PaperSubmissionForm


def assign_document_to_reviewer(request, conference):
    if request.user.is_authenticated:
        document = get_document_to_assign(conference)
        if document:
            # Create an instance of Assigned
            assignment = Assigned(document=document, reviewer=request.user)
            assignment.save()
            return redirect("reviewer_dashboard")
        else:
            messages.error(request, "No document available for assignment.")
    else:
        return redirect("login")
    messages.error(request, "Authenticated user is required.")
    return redirect("home")


def get_document_to_assign(conference_id):
    return Document.objects.filter(
        conference_id=conference_id, reviewer__isnull=True
    ).first()
