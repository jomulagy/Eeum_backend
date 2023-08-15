from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from message.models import Message
import os

class User(AbstractUser):
    age = models.IntegerField()
    nickname = models.CharField(max_length=100, null=True)
    level = models.CharField(max_length=100,null = True, default="돌멩이")
    point = models.IntegerField(null = True, default = 0)
    image = models.ImageField(upload_to='user',null = True)

    prefix = ["귀여운","멋있는","세련된","용감한","소심한","까다로운","잘생긴","못생긴","똑똑한","엉뚱한"]
    subfix = ["원숭이","코끼리","강아지","고양이","거북이","호랑이","햄스터","지렁이","달팽이","토끼","팬더"]

    def set_image(self,folder_name):
        current_directory = os.getcwd()  # 현재 디렉토리의 경로
        parent_directory = os.path.dirname(current_directory)
        folder_name = "강아지"  # 찾을 폴더의 이름
        search_path = os.path.join(parent_directory,"media/profile")  # 검색을 시작할 경로
        for dirs in os.listdir(search_path):
            if dirs == folder_name:
                found_folder_path = os.path.join(search_path, folder_name)
                break
            else:
                found_folder_path = None
        random_choice = random.choice([0, 1])

        image_path = os.listdir(found_folder_path)[random_choice]
        image = Image.open(image_path)
        self.image = image
        self.save()

    def set_nickname(self):
        random_prefix = random.choice(self.prefix)
        random_subfix = random.choice(self.subfix)
        self.set_image(random_subfix)
        self.nickname = random_prefix + " " + random_subfix
        self.save()

    def set_point(self,point):
        self.point+=point
        self.save()
        message = Message(user = self)
        message.save()
        message.get_point(point)

        grade = self.level_up_test()
        if grade:
            message = Message(user = self)
            message.save()
            message.grade_imminent(grade)

        prev_level = self.level
        if prev_level!= self.set_level():
            message = Message(user = self)
            message.save()
            message.update_level(self.level)

    def level_up_test(self):
        if self.point == 99990:
            return "에메랄드"
        elif self.point == 69990:
            return "다이아몬드"
        elif self.point == 34990:
            return "토파즈"
        elif self.point == 14990:
            return "자수정"
        elif self.point == 6990:
            return "진주"
        elif self.point == 2990:
            return "산호"
        elif self.point == 1490:
            return "청금석"
        elif self.point == 490:
            return "대리석"
        else:
            return None

    def set_level(self):
        if self.point >= 100000:
            self.level = "에메랄드"
            self.save()
            return self.level
        elif self.point >= 70000:
            self.level = "다이아몬드"
            self.save()
            return self.level
        elif self.point >= 35000:
            self.level = "토파즈"
            self.save()
            return self.level
        elif self.point >= 15000:
            self.level = "자수정"
            self.save()
            return self.level
        elif self.point >= 7000:
            self.level = "진주"
            self.save()
            return self.level
        elif self.point >= 3000:
            self.level = "산호"
            self.save()
            return self.level
        elif self.point >= 1500:
            self.level = "청금석"
            self.save()
            return self.level
        elif self.point >= 500:
            self.level = "대리석"
            self.save()
            return self.level
        else:
            self.level = "돌멩이"
            self.save()
            return self.level
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
