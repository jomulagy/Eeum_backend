from django.urls import path
from .views import *

urlpatterns = [
    path("",MessageList.as_view()),
]
