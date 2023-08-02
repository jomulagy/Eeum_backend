from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from question.models import *

class QuestionCreateView(View):

    def post(self, request:HttpRequest) -> HttpResponse:


class QuestionListView(View):
    "/create"

    def post(self, request:HttpRequest) -> HttpResponse:
        """질문/조회"""
