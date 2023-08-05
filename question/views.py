from http import HTTPStatus
from django.views.generic import View
from django.http import JsonResponse
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from question.models import *
from word.models import *
from question.serializers import *

@permission_classes((AllowAny,))
class QuestionListView(APIView):

    def post(self, request):
        """전체 질문/조회"""
        entity = Question.objects.filter(type = request.data["type"])
        if request.data["sort"] == "최신":
            entity = entity.order_by("-created_at")
        else:
            entity = entity.order_by("-view")
        resp = QuestionSerializer(entity, many=True).data
        return Response(resp)

@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class QuestionCreateView(APIView):

    def post(self, request):
        """질문/생성"""
        try:
            serializer = QuestionCreateSerializer(data=request.data)
            if serializer.is_valid():
                entity = serializer.save()
                entity.author = request.user
                if entity.type == "질문":
                    entity.word = Word.objects.get(id=request.data["word_id"])
                else:
                    entity.word = None
                entity.save()
                return Response(QuestionSerializer(entity).data)
            
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

@permission_classes((AllowAny,))   
class QuestionDetailListView(APIView):

    def post(self, request):
        """질문 상세"""
        try: 
            entity = Question.objects.get(id = request.data["question_id"])
            resp = QuestionDetailSerializer(entity).data
            return Response(resp)

        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])        
class CommentCreatView(APIView):

    def post(self, request):
        """댓글/생성"""
        try:
            serializer = CommentCreateSerializer(data=request.data)
            if serializer.is_valid():
                entity = serializer.save()
                entity.author = request.user
                entity.question = Question.objects.get(id=request.data["question_id"])
                entity.save()
                return Response(CommentSerializer(entity).data)
            
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

