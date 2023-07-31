from django.contrib.auth.models import AbstractUser
from django.db import models
from word.models import Word
import random

class User(AbstractUser):
    age = models.IntegerField(max_length=3) #나이 제한을 두어야 할까?
    nickname = models.CharField(max_length=12, null=True)
    level = models.CharField(max_length=100,null = True, default="")
    point = models.IntegerField(null = True, default = 0)
    image = models.ImageField(upload_to='user',null = True)

    prefix = ["귀여운","멋있는","세련된","용감한","소심한","까다로운","잘생긴","못생긴","똑똑한","엉뚱한"]
    subfix = ["원숭이","코끼리","강아지","고양이","거북이","호랑이","햄스터","지렁이","달팽이","토끼","팬더"]

    def set_nickname(self):
        random_prefix = random.choice(self.prefix)
        random_subfix = random.choice(self.subfix)

        self.nickname = random_prefix + " " + random_subfix
        self.save()

    def set_level(self):
        if self.point >= 100000:
            self.level = "에메랄드"
            self.save()
        elif self.point >= 70000:
            self.level = "다이아몬드"
            self.save()
        elif self.point >= 35000:
            self.level = "토파즈"
            self.save()
        elif self.point >= 15000:
            self.level = "자수정"
            self.save()
        elif self.point >= 7000:
            self.level = "진주"
            self.save()
        elif self.point >= 3000:
            self.level = "산호"
            self.save()
        elif self.point >= 1500:
            self.level = "청금석"
            self.save()
        elif self.point >= 500:
            self.level = "대리석"
            self.save()
        else:
            self.level = "돌멩이"
            self.save()
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
