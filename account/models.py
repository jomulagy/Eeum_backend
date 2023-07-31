from django.contrib.auth.models import AbstractUser
from django.db import models
from word.models import Word

# Create your models here.
class User(AbstractUser):
    requests = models.ManyToManyField("utils.Request",related_name = "users",null = True)
    age = models.IntegerField(max_length=3, null=False) #나이 제한을 두어야 할까?
    nickname = models.CharField(max_length=12, null=False)
    level = models.CharField(max_length=100)
    point = models.IntegerField()
    image = models.ImageField(upload_to='uploads/') #저장 위치를 어디로?

class Question(models.Model):
    content = models.CharField(max_length=500)
    word = models.OneToOneField(Word,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    views = models.IntegerField()
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

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
