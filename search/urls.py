from django.urls import path
from .views import *

urlpatterns = [
    path("list/",SearchWordList.as_view()),
    path("exists/",SearchWord.as_view()),

]
