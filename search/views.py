from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from question.models import Question
from question.serializers import QuestionSerializer
from word.models import Word
from rest_framework.response import Response
from .serializers import WordSerializer
from django.db.models.functions import Length
from django.db.models import Value

@permission_classes((AllowAny,))
class SearchWordList(APIView):
    def post(self,request):
        keyword = request.data["keyword"]
        words = Word.objects.filter(title__icontains = keyword)
        words = words.annotate(search_accuracy=Length('title') - Length(Value(keyword)))  # 검색어와 일치하는 문자 수를 계산하여 새로운 필드 추가
        words = words.order_by('search_accuracy')  # 검색 정확도 순으로 정렬
        response = WordSerializer(words,many = True).data
        return Response(response)

@permission_classes((AllowAny,))
class SearchWord(APIView):
    def post(self,request):
        keyword = request.data["keyword"]
        if keyword == '':
            response = {
                "is_exists" : True
            }
        elif Word.objects.filter(title = keyword).exists():
            words = Word.objects.get(title = keyword)
            word = WordSerializer(words).data
            response = {
                "is_exists" : True,
                "word" : word
            }
        else:
            response = {
                "is_exists" : False
            }
        return Response(response)

@permission_classes((AllowAny,))
class searchQuestion(APIView):
    def post(self,request):
        keyword = request.data["keyword"]
        words = Question.objects.filter(title__icontains = keyword,type = "등록 요청")
        words = words.annotate(search_accuracy=Length('title') - Length(Value(keyword)))  # 검색어와 일치하는 문자 수를 계산하여 새로운 필드 추가
        words = words.order_by('search_accuracy')  # 검색 정확도 순으로 정렬
        response = QuestionSerializer(words,many = True).data
        return Response(response)
