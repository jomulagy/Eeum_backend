from rest_framework import serializers
from django.conf import settings

from question.models import Question
from word.models import Edit
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["age","nickname","level"]

class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id","age","nickname","image","level","point"]

    def get_image(self,obj):
        if obj.image:
            return settings.HOST + obj.image.url
        else:
            return None

class EditEasySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Edit
        fields = ["title","created_at"]

    def get_created_at(self,obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M")

class QuestionEasySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ["title","created_at"]

    def get_created_at(self,obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M")

