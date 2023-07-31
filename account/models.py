from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    age = models.IntegerField(max_length=3) #나이 제한을 두어야 할까?
    nickname = models.CharField(max_length=12, null=True)
    level = models.CharField(max_length=100,null = True, default="")
    point = models.IntegerField(null = True, default = 0)
    image = models.ImageField(upload_to='uploads/',null = True) #저장 위치를 어디로?

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
