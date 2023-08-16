from http import HTTPStatus
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework.views import APIView
# from django.views.generic import View, UpdateView
from word.models import *

from word.serializers import *
from message.models import Message
from question.models import Question, Question_Likes
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

        if Word.objects.get(id=word_id).likes.filter(id =request.user.id).exists():
            print("like")
            word.likes.remove(request.user)
            word.save()
        else:
            print("dislike")
            word.likes.add(request.user)
            word.save()
        return Response({
            "likes":word.likes.all().count()
        })


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
                        "word": WordEasySerializer(entity, many=True).data
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
            return Response({
                        "data": WordEasySerializer(words, many=True).data
                    })
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
                    "data":WordEasySerializer(words, many=True).data

                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

@permission_classes((AllowAny,))
class WordDetailView(APIView):
    "detail/"

    def post(self, request):
        """단어/ 상세"""

        word_id=request.data["word_id"]
        word= Word.objects.get(pk=int(word_id))
        word.views+=1 # 조회수 증가
        word.save()
        # print(WordSerializer(word).data)

        return Response(WordSerializer(word).data)



@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class WordCreateView(APIView):
    "/create"

    def post(self, request):
        print(request.POST)
        print(request.FILES)
        """단어/ 생성"""
        if Word.objects.filter(title = request.POST.get("title")).exists():
            return JsonResponse(
                status=HTTPStatus.BAD_REQUEST,
                data={
                    "message": "이미 존재하는 단어 입니다.",
                }
            )
        serializer = WordCreateSerializer(data=request.POST)
        print(serializer)
        if serializer.is_valid():
            word = serializer.save()
            word.author = request.user
            print(word.author)
            for age in request.POST.getlist('age'):
                word.age.add(Age.objects.get(value=age))
            if "image" in request.FILES:
                word.image = request.FILES["image"]
            word.save()
            request.user.set_point(50)
            if Question.objects.filter(type = "등록 요청",title = word.title).exists():
                question = Question.objects.get(type = "등록 요청",title = word.title)
                question.word = word
                question.save()
                message = Message(user = question.author)
                message.create_word(word)
                message.save()
                for like in Question_Likes.objects.filter(question = question):
                    message = Message(user = like.author)
                    message.create_word(word)
                    message.save()

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
            request.user.set_point(50)

            return JsonResponse(
                status=HTTPStatus.OK,
                data={
                    "data": {
                        "word": WordSerializer(word).data
                    },
                    "message": "단어가 수정되었습니다.",
                },
            )
        else:
            return Response(status = 401,data = {"error":"작성자만 수정할 수 있음"})









class EditLikesView(APIView):
    def post(self, request):
        edit_id = request.data["edit_id"]
        edit= Edit.objects.get(id=edit_id)

        if Edit.objects.filter(id=edit_id, likes=request.user).exists():
            edit.likes.remove(request.user)
            edit.save()
        else:
            edit.likes.add(request.user)
            edit.save()
        return Response(edit.likes.all().count())


@permission_classes((AllowAny,))
class EditMostView(APIView):
    "edit/most_views/"

    def get(self, request:HttpRequest) -> HttpResponse:
        """edit/조회수 조회
        
        조회수 많은 순
        """

        try:
            edits = Edit.objects.all().order_by('-views')
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "word": EditSerializer(edits, many=True).data
                    },
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

@permission_classes((AllowAny,))
class EditRecentView(APIView):
    "edit/recent/"

    def get(self, request:HttpRequest) -> HttpResponse:
        """edit/기간별 조회
        
        최근 등록된 순
        """
        try:
            edits = Edit.objects.all().order_by('-created_at')
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "edit": EditSerializer(edits, many=True).data
                    },
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})

@permission_classes((AllowAny,))
class EditDetailView(APIView):
    "edit/detail/"

    def post(self, request):
        """수정요청 / 상세"""
        try:
            edit_id=request.data["edit_id"]
            edit= Edit.objects.get(pk=edit_id)
            edit.views+=1 # 조회수 증가
            edit.save()
            print(edit)

            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "edit": EditSerializer(edit).data
                    },
                },
            )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})




@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class EditCreateView(APIView):
    "/edit/create/"

    def post(self, request):
        """Edit(수정요청) /생성"""
        serializer= EditCreateSerializer(data=request.data)
        if serializer.is_valid():
            word_id= request.data["word_id"]   # edit.word.add(word) #pk가 word_id인 class word 가져와
            word= Word.objects.get(pk=word_id)
            edit= serializer.save()
            edit.word = word
            edit.author = request.user
            edit.save()
            message = Message(user = word.author)
            message.get_edit(edit)
            message.save()
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "edit": EditSerializer(edit).data
                    }
                }
            )
        return JsonResponse(
            status=HTTPStatus.BAD_REQUEST,
            data={
                "message": "유효하지 않은 형식입니다.",
            }
        )


@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class EditUpdateView(APIView):
    "edit/<int:edit_id>/update/"
    def put(self, request, **kwargs):
        """Edit(수정요청) /수정"""
        try:
            edit_id = kwargs["edit_id"]
            edit = get_object_or_404(Edit, pk=edit_id)

            if edit.author == request.user :
                edit.title = request.data.get('title', edit.title)
                edit.content = request.data.get('content', edit.content)
                edit.save()
                request.user.set_point(5)

                return JsonResponse(
                    status=HTTPStatus.OK,
                    data={
                        "data":{
                            "word": EditSerializer(edit).data
                        },
                        "message": "수정요청이 수정되었습니다.",
                    },
                )
        except :
            return JsonResponse(status=HTTPStatus.FORBIDDEN, data={"message": "권한이 없습니다."})



@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class EditDeleteView(APIView):
    "edit/delete/"

    def post(self, request):
        """수정요청 / 삭제"""
        try:
            edit_id=request.data["edit_id"]
            edit= Edit.objects.get(pk=edit_id)
            if edit.author == request.user:
                edit.delete()
                return JsonResponse(
                    status= HTTPStatus.OK,
                    data={
                        "data":{
                            "message": "수정요청이 삭제되었습니다.",
                        },
                    },
                )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})
        except :
            return JsonResponse(status=HTTPStatus.FORBIDDEN, data={"message": "권한이 없습니다."})


class CommentLikesView(APIView):
    def post(self, request):
        comment_id = request.data["comment_id"]
        comment= Comment.objects.get(id=comment_id)

        if Comment.objects.filter(id=comment_id, likes=request.user).exists():
            comment.likes.remove(request.user)
            comment.save()
        else:
            comment.likes.add(request.user)
            comment.save()
        return Response(comment.likes.all().count())


@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class CommentCreateView(APIView):
    "comment/create/"
    ##Body에 edit_id 넣어야해

    def post(self, request): ##body에 edit_id 받아야돼
        """Comment(수정요청 답글) /생성create"""
        serializer= CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            edit_id= request.data["edit_id"]   # edit.word.add(word) #pk가 word_id인 class word 가져와
            edit= Edit.objects.get(pk=edit_id)
            comment =serializer.save()
            comment.edit= edit
            comment.author= request.user
            comment.save()
            message = Message(user = edit.author)
            message.create_answer(edit,comment)
            message.save()
            likes = edit.likes.all()
            for like in likes:
                message = Message(user=like.user)
                message.get_answer(edit)
                message.save()
            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "edit": CommentSerializer(comment).data
                    }
                }
            )
        return JsonResponse(
            status=HTTPStatus.BAD_REQUEST,
            data={
                "message": "유효하지 않은 형식입니다.",
            }
        )

@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class CommentDetaileView(APIView):
    "comment/detail/"
    ##Body에 edit_id 넣어야해
    def post(self, request):
        """답글 / 상세"""
        try:
            comment_id = request.data["comment_id"]
            comment = Comment.objects.get(pk= comment_id)
            comment.views += 1
            comment.save()

            print(comment)

            return JsonResponse(
                status= HTTPStatus.OK,
                data={
                    "data":{
                        "comment": CommentSerializer(comment).data
                    },
                },
            )
        except (KeyError, ValueError):
                return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})







#수정

@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class CommentUpdateView(APIView):
    "comment/<int:comment_id>/update/"
    def put(self, request, **kwargs):
        """Comment(답글) /수정"""
        try:
            comment_id = kwargs["comment_id"]
            comment = get_object_or_404(Comment, pk=comment_id)

            if comment.author == request.user :
                comment.content = request.data.get('content', comment.content)
                comment.save()

                return JsonResponse(
                    status=HTTPStatus.OK,
                    data={
                        "data":{
                            "word": CommentSerializer(comment).data
                        },
                        "message": "답글이 수정되었습니다.",
                    },
                )
        except :
            return JsonResponse(status=HTTPStatus.FORBIDDEN, data={"message": "권한이 없습니다."})



# 삭제
@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class CommentDeleteView(APIView):
    "comment/delete/"

    def post(self, request):
        """답글 / 삭제"""
        try:
            comment_id=request.data["comment_id"]
            comment= Comment.objects.get(pk=comment_id)
            if comment.author == request.user:
                comment.delete()
                return JsonResponse(
                    status= HTTPStatus.OK,
                    data={
                        "data":{
                            "message": "답글이 삭제되었습니다.",
                        },
                    },
                )
        except (KeyError, ValueError):
            return JsonResponse(status= HTTPStatus.BAD_REQUEST, data={})
        except :
            return JsonResponse(status=HTTPStatus.FORBIDDEN, data={"message": "권한이 없습니다."})
