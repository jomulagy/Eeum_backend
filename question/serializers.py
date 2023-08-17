
from rest_framework import serializers
from .models import Question, Comment
from account.models import User
from word.models import Word, Age
from django.conf import settings

class AuthorSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id","nickname", "image"]
    
    def get_image(self, obj):
        if obj.image:
            return getattr(settings,"HOST")+obj.image.url
        else:
            return None


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ["id","author", "created_at", "views", "answers", "title", "content", "likes"]
    
    def get_author(self,obj): #obj: 
        return AuthorSerializer(obj.author).data
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y/%m/%d")
    
    def get_answers(self, obj):
        return obj.comment_set.all().count()

    def get_likes(self, obj):
        return obj.question_likes_set.all().count()
    
class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["content", "title", "type"]

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ["id","created_at", "author", "content", "likes"]
    
    def get_author(self,obj):
        return AuthorSerializer(obj.author).data
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M")
    
    def get_likes(self, obj):
        return obj.comment_likes_set.all().count()

class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields = ["value"]
    

class WordSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Word
        fields = ["id","title", "content", "age", "likes"]
    
    def get_age(self,obj):
        ages = AgeSerializer(obj.age.all(), many=True).data
        return [age["value"] for age in ages]
    
    def get_likes(self, obj):
        return obj.likes.all().count()

class QuestionDetailSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    word = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ["id","question", "word", "comments"]
    
    def get_question(self,obj):
        return QuestionSerializer(obj).data
    
    def get_word(self,obj):
        if obj.word:
            print("obj.word : ",obj.word)
            print("word :",WordSerializer(obj.word).data)
            return WordSerializer(obj.word).data
        else:
            return None
    
    def get_comments(self,obj):
        return CommentSerializer(obj.comment_set.all(), many=True).data

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id","content"]
