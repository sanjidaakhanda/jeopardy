from django.shortcuts import render
from quizzes.models import Quiz

# Create your views here.
def home(request):
    quiz = Quiz.objects.all()
    para = {'quiz' : quiz}
    return render(request, "home.html", para)