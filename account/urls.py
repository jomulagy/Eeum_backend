from django.urls import path
from .views import *
app_name = "account"

urlpatterns = [
    path("kakao/callback/",KaKaoCallBackView.as_view(),name = "kakao-callback"),
    path("refresh/",RefreshAccessToken.as_view()),
    path("logout/",LogoutView.as_view()),
    path("user/",UserInfo.as_view()),
    path("user/word/",UserWord.as_view()),
    path("user/word/list/",UserWordList.as_view()),
    path("user/question/",UserQuestion.as_view()),
    path("user/question/list/",UserQuestionList.as_view()),
    path("user/edit/",UserEdit.as_view()),
    path("user/edit/list/",UserEditList.as_view()),

]
