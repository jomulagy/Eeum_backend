from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login

from .models import User

import requests

class KaKaoView(View):
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id="
        redirect_uri = "http://127.0.0.1:8000/account/kakao/callback/"
        client_id = "86a527ceaedd9951ed011a5f0011bb5d"

        return redirect(f"{kakao_api}{client_id}&redirect_uri={redirect_uri}")

class KaKaoCallBackView(View):
    def get(self, request):
        data = {
            "grant_type": "authorization_code",
            "client_id": "86a527ceaedd9951ed011a5f0011bb5d",
            "redirect_uri" : "http://127.0.0.1:8000/account/kakao/callback/",
            "code" : request.GET["code"]
        }

        kakao_token_api = "https://kauth.kakao.com/oauth/token"

        ACCESS_TOKEN = requests.post(kakao_token_api,data = data).json()["access_token"]

        kakao_user_api = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization":f"Bearer ${ACCESS_TOKEN}",
            "Content-type" : "application/x-www-form-urlencoded;charset=utf-8"
        }
        user_info = requests.get(kakao_user_api,headers = headers).json()

        username = user_info["id"]
        age = int(user_info["kakao_account"]["age_range"][:2])

        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=None)

        # 로그인 처리
        login(request, user)
        print(username,age)
        return redirect('/')
