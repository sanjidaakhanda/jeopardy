

from django.urls import path
from . import views

urlpatterns = [
 
   path("", views.home, name="home"),
   # path("<int:myid>/", views.quiz, name="quiz"), 
]
