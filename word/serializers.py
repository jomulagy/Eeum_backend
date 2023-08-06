from rest_framework import serializers
from django.utils import timezone
from django.conf import settings


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


class WordSerializer(serializers.ModelSerializer):
    age= serializers.SerializerMethodField()
    likes= serializers.SerializerMethodField()  
    created_at= serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    author=serializers.SerializerMethodField()
    edits= serializers.SerializerMethodField()
    my_words= serializers.SerializerMethodField()
    
    class Meta:
        model = Word
        fields = ["title","mean", "content","age","likes", "views","created_at","image","author","edits","my_words"]

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
        return obj.author.nickname
    def get_edits(self, obj):
        return EditSerializer(obj.edit_set.all().order_by("-created_at"), many=True).data[:4]
    def get_my_words(self,obj):
        return list(obj.author.word_set.all().order_by("-created_at").values_list('title', flat=True))[:4]




class AuthorSerializer(serializers.ModelSerializer):
    image= serializers.SerializerMethodField()

    class Meta:
        model= User
        fields = ["nickname", "image"]

    def get_image(self, obj):
        return settings.HOST + obj.image.url


class EditSerializer(serializers.ModelSerializer):
    author= serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField() 

    class Meta:
        model= Edit
        fields= ["title", "content","views", "author", "created_at", "comment_count", "comment", "likes"]
    
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
        fields= ["content","author","created_at","likes","views"]
    
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