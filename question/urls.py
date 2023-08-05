from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('list/', QuestionListView.as_view()),
    path('questioncreate/', QuestionCreateView.as_view()),
    path('detail/', QuestionDetailListView.as_view()),
    path('commentcreate/', CommentCreatView.as_view()),

]
