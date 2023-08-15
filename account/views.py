from django.shortcuts import redirect
from django.views import View
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from word.models import Edit
from .models import User

import requests

from .serializers import UserSerializer, EditEasySerializer, UserCreateSerializer
from search.serializers import WordSerializer

@permission_classes((AllowAny,))
class KaKaoCallBackView(APIView):
    def post(self, request):
        print(request.data)
        username = str(request.data["id"])
        age = int(request.data["age"][:2])

        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=None,age = age)
            user.set_nickname()
        user.age = age
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
        })

@permission_classes((AllowAny,))
class RefreshAccessToken(APIView):
    def post(self,request):
        refresh_token = request.data["refresh"]
        if not refresh_token:
            return Response({'error': 'Refresh 토큰이 필요합니다'}, status=401)

        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = str(refresh_token.access_token)

            return Response({'access': access_token,'refresh':str(refresh_token)})
        except Exception as e:
            return Response({'error': '유효하지 않은 Refresh 토큰'}, status=401)

@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class UserInfo(APIView):
    def get(self,request):
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data)

    def put(self,request):
        serializer = UserCreateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            user.image = request.FILES.get("image")
            user.save()
            resp = UserSerializer(request.user).data
            return Response(resp, status=200)
        return Response(serializer.errors, status=400)

@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class UserWord(APIView):
    def get(self,request):
        words = request.user.word_set.all()
        response = WordSerializer(words,many = True).data
        return Response(response)

@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class EditList(APIView):
    def get(self,request):
        edits = Edit.objects.filter(author = request.user).order_by("created_at")
        response = EditEasySerializer(edits,many = True).data
        return Response(response)
