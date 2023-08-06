from http import HTTPStatus
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404 
from rest_framework.response import Response

from rest_framework.views import APIView
# from django.views.generic import View, UpdateView
from word.models import *

from word.serializers import *
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json

from rest_framework import generics



# Create your views here.

class WordLikesView(APIView):
    def post(self, request):
        word_id = request.data["word_id"]
        word= Word.objects.get(id=word_id)

        if Word.objects.filter(id=word_id, likes=request.user).exists():
            word.likes.remove(request.user)
            word.save()
        else:
            word.likes.add(request.user)
            word.save()
        return Response(word.likes.all().count())


@permission_classes((AllowAny,))
class WordAllView(APIView):
    "all/"

    def get(self, request:HttpRequest) -> HttpResponse:
        """단어/전체 조회""" 
        try: 
            entity = Word.objects.all()
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "word": WordSerializer(entity, many=True).data
                    },   
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

@permission_classes((AllowAny,))
class WordMostView(APIView):
    "most_views/"
    
    def get(self, request:HttpRequest) -> HttpResponse:
        """단어/조회수 조회
        
        조회수 많은 순
        """ 
                # for age in request.POST.getlist("age"):
                #     word.age.add(Age.objects.get(value=int(age)))
        try: 
            words = Word.objects.order_by('-views')
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "word": WordSerializer(words, many=True).data
                    },   
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

@permission_classes((AllowAny,))
class WordRecentView(APIView):
    "recent/"
    
    def get(self, request:HttpRequest) -> HttpResponse:
        """단어/기간별 조회
        
        최근 등록된 순
        """ 
        try: 
            words = Word.objects.order_by('-created_at')
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "word": WordSerializer(words, many=True).data
                    },   
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

@permission_classes((AllowAny,))
class WordDetailView(APIView):
    "detail/"

    def get(self, request):
        """단어/ 상세"""

        word_id=request.data["word_id"]
        word= Word.objects.get(pk=word_id)
        word.views+=1 # 조회수 증가
        word.save()
        # print(WordSerializer(word).data)

        return Response(WordSerializer(word).data)



@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class WordCreateView(APIView):
    "/create"
    
    def post(self, request):
        """단어/ 생성"""
        serializer = WordCreateSerializer(data=request.POST)
        if serializer.is_valid():
            word = serializer.save()
            word.author = request.user
            for age in request.POST.getlist('age'):
                word.age.add(Age.objects.get(value=int(age)))
            word.image = request.FILES["image"]
            print(request.FILES)
            word.save()

            return JsonResponse(
                status=HTTPStatus.OK,
                data={
                    "data": {
                        "word":WordSerializer(word).data
                    }
                }
            )
        print(serializer.errors)
        return JsonResponse(
            status=HTTPStatus.BAD_REQUEST,
            data={
                "message": "유효하지 않은 형식입니다.",
            }
        )



@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class WordUpdateView(APIView): #UpdateAPIView
    "/update/<int:word_id>" 
    def put(self, request, **kwargs):
        """단어/수정"""
        try: 
            word_id = kwargs["word_id"]
            word = get_object_or_404(Word, pk=word_id)
            if word.author == request.user:
                word.title = request.POST.get('title', word.title)
                for age in request.POST.getlist("age"):
                    word.age.add(Age.objects.get(value=int(age)))
                word.mean = request.POST.get('mean', word.mean)
                word.content = request.POST.get('content', word.content)
                word.image = request.FILES["image"]
                word.save()

                return JsonResponse(
                    status=HTTPStatus.OK,
                    data={
                        "data":{
                            "word": WordSerializer(word).data
                        },
                        "message": "단어가 수정되었습니다.",
                    },   
                )
        except :
            return JsonResponse(status=HTTPStatus.FORBIDDEN, data={"message": "권한이 없습니다."})
        
        serializers = WordSerializer(data=request.data)
        if serializers.is_valid():
            word = serializers.save()
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "word":WordSerializer(request)
                    }
                }
            )
        return JsonResponse(
            status=HTTPStatus.BAD_REQUEST, #유효하지 않은 값
            data={
                "message": "유효하지않은 형식입니다."
            }
        )


class WordUpdateView(View):
    "/update"

    def patch(self, request:HttpRequest) -> HttpResponse:
        """단어/수정
        
        수정할 단어를 선택해서 변경해서 저장
        """