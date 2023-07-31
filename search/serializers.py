from rest_framework import serializers
from word.models import Word

class WordSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Word
        fields = ["id","title","age","content","likes"]

    def get_likes(self,obj):
        return obj.likes.all().count()
