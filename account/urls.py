from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.Signup, name="signup"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),   
    path('add_quiz/', views.add_quiz, name='add_quiz'), 
      
]