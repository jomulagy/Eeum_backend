from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    requests = models.ManyToManyField("utils.Request",related_name = "users",null = True)

    ### 해결된 질문
    # def get_solved_request(self):
    #     return self.requests.filter(word__isnull=False)

    ### 해결 안된 질문
    # def get_solved_request(self):
    #     return self.requests.filter(word__isnull=True)

    ### 안읽은 메세지 개수 구하는 함수
    # def get_unread_messages_count(self):
    #     return self.messages.filter(read=False).count()

    ### 등급 구하는 함수

    # def get_lever(self):
    #     if self.points<뭐시기:
    #         return 뭐시기
    #     elif ...
