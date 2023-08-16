from django.shortcuts import render

from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

import random

from search.serializers import WordSerializer
from vocabulary.models import Vocabulary
from vocabulary.serializers import QuizSerializer
from word.models import Word
from message.models import Message
@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class Vocablulary(APIView):
    def get(self,request):
        vocabularys = list(Vocabulary.objects.filter(user = request.user).values_list("word",flat = True))
        vocabularys = Word.objects.filter(id__in = vocabularys)
        response = WordSerializer(vocabularys,many = True).data
        return Response(response)

    def post(self,request):
        id = request.data.get("id")
        if Vocabulary.objects.filter(user = request.user,word__id = id).exists():
            vocabulary = Vocabulary.objects.filter(word__id = id)
            vocabulary.delete()
            return Response({"message" : "단어장에서 삭제되었습니다"},status=200)
        else:
            vocabulary = Vocabulary(user = request.user,word = Word.objects.get(id = id))
            vocabulary.save()
            return Response({"message" : "단어장에 추가되었습니다"},status=200)


@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class Quiz(APIView):
    def get(self,request):
        vocabularys = Vocabulary.objects.filter(user = request.user)
        vocabularys = random.sample(list(vocabularys),5)
        quizes = QuizSerializer(vocabularys,many = True).data
        vocabularys = [vocabulary.word.id for vocabulary in vocabularys]

        words = Word.objects.filter(id__in = vocabularys)
        words = WordSerializer(words,many=True).data
        response = {
            "quizes" : quizes,
            "words":words
        }
        return Response(data = response)

    def post(self,request):
        request.user.set_point(int(request.data.get("point")))

        return Response(status=200)


