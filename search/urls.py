from django.urls import path
from .views import *

urlpatterns = [
    path("word/",SearchWordList.as_view()),
    path("word/exists/",SearchWord.as_view()),
    path("question/",searchQuestion.as_view()),

]
