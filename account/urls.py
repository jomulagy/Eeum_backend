from django.urls import path
from .views import *
app_name = "account"

urlpatterns = [
    path("kakao/",KaKaoView.as_view(),name = "kakao"),
    path("kakao/callback/",KaKaoCallBackView.as_view(),name = "kakao-callback")
]
