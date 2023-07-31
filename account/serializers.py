from rest_framework import serializers

from word.models import Edit
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["age","nickname","image","level"]

class EditEasySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Edit
        fields = ["title","created_at"]

    def get_created_at(self,obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M")
