from django.urls import path
from word.views import *
from django.views.decorators.csrf import csrf_exempt

app_name = "word"

urlpatterns = [
    path('all/', WordAllView.as_view()),
    path('most_views/', WordMostView.as_view()),
    path('recent/', WordRecentView.as_view()),
    path('detail/', WordDetailView.as_view()),
    path('create/', csrf_exempt(WordCreateView.as_view())),
    path('update/<int:word_id>/', csrf_exempt(WordUpdateView.as_view())),


    path('edit/most_views/', csrf_exempt(EditMostView.as_view())),
    path('edit/recent/', csrf_exempt(EditRecentView.as_view())),
    path('edit/detail/', csrf_exempt(EditDetailView.as_view())),
    path('edit/create/', csrf_exempt(EditCreateView.as_view())),
    path('edit/<int:edit_id>/update/', csrf_exempt(EditUpdateView.as_view())),
    path('edit/delete/', csrf_exempt(EditDeleteView.as_view())),


    path('comment/create/', csrf_exempt(CommentCreateView.as_view())),
    path('comment/detail/', csrf_exempt(CommentDetaileView.as_view())),
    path('comment/<int:comment_id>/update/', csrf_exempt(CommentUpdateView.as_view())),
    path('comment/delete/', csrf_exempt(CommentDeleteView.as_view())),

    path('like/', csrf_exempt(WordLikesView.as_view())),
    path('edit/like/', csrf_exempt(EditLikesView.as_view())),
    path('comment/like/', csrf_exempt(CommentLikesView.as_view())),
]