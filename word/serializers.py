from rest_framework import serializers
from django.utils import timezone
from django.conf import settings
from django.db.models import Count

from question.models import Question
from vocabulary.models import Vocabulary
from word.models import * 
from account.models import User


class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields= ["value"]



class WordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Word
        fields= ["title", "mean", "content"]

class WordAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        fields = ["id","nickname", "level"]

class QuestionsEasySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ["id","title","created_at"]

    def get_created_at(self,obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M")

class WordSerializer(serializers.ModelSerializer):
    age= serializers.SerializerMethodField()
    likes= serializers.SerializerMethodField()  
    created_at= serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    author=serializers.SerializerMethodField()
    questions= serializers.SerializerMethodField()
    edits= serializers.SerializerMethodField()
    my_words= serializers.SerializerMethodField()
    like_ages = serializers.SerializerMethodField()
    is_likes = serializers.SerializerMethodField()
    is_vocabulary = serializers.SerializerMethodField()
    class Meta:
        model = Word
        fields = ["id","title","mean", "content","age","likes", "views","created_at","image","author","edits","questions","my_words","like_ages","is_likes","is_vocabulary"]


    def get_age(self, obj):
        age= AgeSerializer(obj.age.all(), many=True).data
        return [item["value"] for item in age]
    def get_likes(self, obj):
        return obj.get_likes()
    def get_created_at(self,obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M")
    def get_image(self, obj):
        if obj.image:
            return settings.HOST + obj.image.url
        else:
            return ""
    def get_author(self, obj):
        return WordAuthorSerializer(obj.author).data
    def get_questions(self, obj):
        return QuestionsEasySerializer(obj.edit_set.all().order_by("-created_at"), many=True).data[:4]
    def get_edits(self, obj):
        return EditSerializer(obj.edit_set.all().order_by("-created_at"), many=True).data[:4]
    def get_my_words(self,obj):
        return list(obj.author.word_set.all().order_by("-created_at").values_list('title', flat=True))[:4]
    def get_like_ages(self,obj):
        ages = list(obj.likes.values('age').annotate(count=Count('age')))
        data = {
            "10":0,
            "20":0,
            "30":0,
            "40":0,
            "50":0,

        }
        for age in ages:
            if str(age['age']) in data:
                data[str(age['age'])] = age['count']
        return data
    def get_is_likes(self,obj):
        request = self.context.get('request')
        if request.user.is_authenticated and obj.likes.filter(id = request.user.id).exists():
            return True
        else:
            return False

    def get_is_vocabulary(self,obj):
        request = self.context.get('request')
        print(request.user)
        if request.user.is_authenticated and Vocabulary.objects.filter(user = request.user,word = obj).exists():
            return True
        else:
            return False

class WordEasySerializer(serializers.ModelSerializer):
    age= serializers.SerializerMethodField()
    likes= serializers.SerializerMethodField()

    class Meta:
        model = Word
        fields = ["id","title","mean","age","likes"]

    def get_age(self, obj):
        age= AgeSerializer(obj.age.all(), many=True).data
        return [item["value"] for item in age]
    def get_likes(self, obj):
        return obj.get_likes()

class AuthorSerializer(serializers.ModelSerializer):
    image= serializers.SerializerMethodField()

    class Meta:
        model= User
        fields = ["id","nickname", "image"]

    def get_image(self, obj):
        if obj.image:
            return settings.HOST + obj.image.url
        else:
            return None


class EditSerializer(serializers.ModelSerializer):
    author= serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField() 

    class Meta:
        model= Edit
        fields= ["id","title", "content","views", "author", "created_at", "comment_count", "comment", "likes"]
    
    def get_author(self,obj): #프로필 사진, 닉네임
        return AuthorSerializer(obj.author).data
    def get_created_at(self,obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M")
    def get_comment_count(self,obj):
        return obj.comment_set.all().count()
    def get_comment(self, obj):
        return CommentSerializer(obj.comment_set.all(), many=True).data
    def get_likes(self, obj):
        return obj.get_likes()


class EditCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Edit
        fields= ["title", "content"]
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField() 
    created_at = serializers.SerializerMethodField() 
    likes = serializers.SerializerMethodField() 

    class Meta:
        model= Comment
        fields= ["id","content","author","created_at","likes","views"]
    
    def get_author(self, obj):
        return AuthorSerializer(obj.author).data
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M")
    def get_likes(self, obj):
        return obj.get_likes()


class CommentCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Comment
        fields=["content"]
