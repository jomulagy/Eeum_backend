from django.urls import path
from .views import *
app_name = "account"

urlpatterns = [
    path("kakao/callback/",KaKaoCallBackView.as_view(),name = "kakao-callback"),
    path("refresh/",RefreshAccessToken.as_view()),

    path("user/",UserInfo.as_view()),
    path("user/word/",UserWord.as_view()),
    path("user/question/",UserQuestionList.as_view()),
    path("user/edit/",EditList.as_view()),

]
