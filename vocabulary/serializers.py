import random

from rest_framework import serializers
from word.models import Word
from .models import Vocabulary

class QuizSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    choices = serializers.SerializerMethodField()
    class Meta:
        model = Vocabulary
        fields = ["title","choices"]

    def get_title(self,obj):
        return str(obj.word.title) + "의 뜻은?"

    def get_choices(self,obj):
        choices = []
        choices.append({"choice":obj.word.mean,"is_answer":True})
        wrongs = Word.objects.exclude(id = obj.word.id)
        wrongs = random.sample(list(wrongs),2)

        choices+=[{"choice":wrong.mean,"is_answer":False} for wrong in wrongs]
        random.shuffle(choices)
        return choices



