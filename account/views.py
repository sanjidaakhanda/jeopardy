from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.http import JsonResponse
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm
from django.forms import inlineformset_factory
from django.contrib import messages  


# Create your views here.


def Signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password != confirm_password:
            messages.error(request, "Password and confirm password do not match.")
            return redirect('signup')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, f"Account created for {username}. You can now log in.")
        return redirect('login')

    return render(request, "signup.html")


# def Signup(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#     if request.method=="POST":   
#         username = request.POST['username']
#         email = request.POST['email']
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         password = request.POST['password1']
#         confirm_password = request.POST['password2']
        
#         if password != confirm_password:
#             return redirect('/register')
        
#         user = User.objects.create_user(username, email, password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()
#         return render(request, 'login.html')  
#     return render(request, "signup.html")

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html") 
    return render(request, "login.html")


def add_quiz(request):
    if request.method=="POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            obj = form.instance
            return render(request, "add_quiz.html", {'obj':obj})
    else:
        form=QuizForm()
    return render(request, "add_quiz.html", {'form':form})
    
@login_required
def Logout(request):
    logout(request)
    return redirect('home')
