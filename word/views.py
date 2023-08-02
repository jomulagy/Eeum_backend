from http import HTTPStatus

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from word.models import *
from word.serializers import *
from django.core.exceptions import ObjectDoesNotExist, ValidationError


# Create your views here.
class WordView(View):
    "/"

    def get(self, request:HttpRequest) -> HttpResponse:
        """단어/조회""" 
        try: 
            entity = Word.objects.all()
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "word": WordSerializer(entity)
                    },   
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})
        




class WordCreateView(View):
    "/create"

    def post(self, request:HttpRequest) -> HttpResponse:
        """단어/생성"""
        
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
        try:
                    


#삭제는 안하나???