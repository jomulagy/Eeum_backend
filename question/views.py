from http import HTTPStatus
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from question.models import *
from question.serializers import *

class UserNotLoggedInException(Exception):
    pass

def check_user_logged_in(request):
    if not request.user.is_authenticated:
        raise UserNotLoggedInException()

class QuestionListView(View):

    def post(self, request:HttpRequest) -> HttpResponse:
        """질문/조회"""
        try: 
            entity = Question.objects.all()
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "Question": serializeQuestion(entity)
                    },   
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

class top5QuestionListView(View):

    def post(self, request:HttpRequest) -> HttpResponse:
        """조회수가 가장 높은 질문 top 4/조회"""
        try: 
            entity = Question.objects.order_by('-views')[:5]
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "Question": serializeQuestion(entity)
                    },   
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})
        
class top5QuestionListView(View):

    def post(self, request:HttpRequest) -> HttpResponse:
        """가장 최근에 올라온 질문 top4/조회"""
        try: 
            entity = Question.objects.order_by('-created_at')[:5]
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "Question": serializeQuestion(entity)
                    },   
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

class QuestionCreateView(View):

    def post(self, request:HttpRequest) -> HttpResponse:
        """질문/생성"""
        try:
            check_user_logged_in(request)

        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})
        except UserNotLoggedInException:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)
        
class CommentListView(View):

    def post(self, request:HttpRequest) -> HttpResponse:
        """댓글/조회"""
        try: 
            entity = Comment.objects.all()
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "Comment": serializeComment(entity)
                    },   
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})
        
class CommentCreatView(View):

    def post(self, request:HttpRequest) -> HttpResponse:
        """댓글/생성"""

