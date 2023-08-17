from rest_framework import serializers
from word.models import Word
from word.models import Age

class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields = ["value"]

class WordSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    ages = serializers.SerializerMethodField()
    class Meta:
        model = Word
        fields = ["id","title","ages","mean","likes"]

    def get_likes(self,obj):
        return obj.likes.all().count()

    def get_ages(self,obj):
        ages = obj.age.all()
        ages = AgeSerializer(ages,many = True).data
        ages = [age["value"] for age in ages ]
        return ages
