from django.utils import timezone
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ["id","created_at","read","content"]

    def get_created_at(self,obj):
        now = timezone.now()
        time_difference = now - obj.created_at
        if time_difference.total_seconds() < 60:
            return("방금 전")
        elif time_difference.total_seconds() < 60 * 60:
            minutes = int(time_difference.total_seconds() / 60)
            return(f"{minutes}분 전")
        elif time_difference.total_seconds() < 60 * 60 * 24:
            hours = int(time_difference.total_seconds() / (60 * 60))
            return(f"{hours}시간 전")
        elif time_difference.total_seconds() < 60 * 60 * 24 * 30:
            days = int(time_difference.total_seconds() / (60 * 60 * 24))
            return(f"{days}일 전")
        elif time_difference.total_seconds() < 60 * 60 * 24 * 365:
            months = int(time_difference.total_seconds() / (60 * 60 * 24 * 30))
            return(f"{months}달 전")
        else:
            years = int(time_difference.total_seconds() / (60 * 60 * 24 * 365))
            return(f"{years}년 전")
