from django.urls import path
from .views import *

urlpatterns = [
    path("",Vocablulary.as_view()),
    path("quiz/",Quiz.as_view()),
]
