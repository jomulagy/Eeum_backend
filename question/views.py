from http import HTTPStatus
from django.views.generic import View
from django.core import serializers
from django.http import JsonResponse
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from question.models import *
from word.models import *
from message.models import Message
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
        print(request.data)
        serializer = QuestionCreateSerializer(data=request.data)
        if serializer.is_valid():
            entity = serializer.save()
            entity.author = request.user
            if entity.type == "질문":
                word = Word.objects.get(id=request.data["word_id"])
                entity.word = word
                message = Message(user = word.author)
                message.get_question(word.title)
                message.save()
            else:
                entity.word = None
            entity.save()

            return Response(QuestionSerializer(entity).data)
        else:
            return Response(status=400)


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
                question = Question.objects.get(id=request.data["question_id"])
                entity.question = question
                entity.save()
                request.user.set_point(25)

                message = Message(user = question.author)
                message.create_answer(question.title)
                message.save()

                likes = Question_Likes.objects.filter(question = question)
                for like in likes:
                    message = Message(user = like.user)
                    message.get_answer(question.title)
                    message.save()
                return Response(CommentSerializer(entity).data)
            
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])      
class QuestionLikeView(APIView):
    
    def post(self, request):
        try:
            entity = Question.objects.get(id = request.data["question_id"])
            if Question_Likes.objects.filter(user = request.user, question = entity).exists():
                like = Question_Likes.objects.get(user = request.user, question = entity)
                like.delete()
                return JsonResponse({'like': '0'})
            else:
                like = Question_Likes(user = request.user, question = entity)
                like.save()
                return JsonResponse({'like': '1'})

        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])      
class CommentLikeView(APIView):
    
    def post(self, request):
        try:
            entity = Comment.objects.get(id = request.data["comment_id"])
            if Comment_Likes.objects.filter(user = request.user, comment = entity).exists():
                like = Comment_Likes.objects.get(user = request.user, comment = entity)
                like.delete()
                return JsonResponse({'like': '0'})
            else:
                like = Comment_Likes(user = request.user, comment = entity)
                like.save()
                return JsonResponse({'like': '1'})
           
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})
