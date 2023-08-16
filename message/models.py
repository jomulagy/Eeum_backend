from django.db import models

class Message(models.Model):
    content = models.CharField(max_length=100,blank = True, default = "")
    read = models.BooleanField(default=False)
    user = models.ForeignKey("account.User",on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length = 100)
    target_id = models.IntegerField(null = True)

    def create_answer(self, obj, comment):
        self.content = f"{obj.title}에 대한 답변이 등록되었습니다."
        self.type = "댓글"
        self.target_id = comment.id
        self.save()

    def update_level(self, grade):
        self.content = f"{self.user.nickname}님의 등급이 {grade}으로 조정되었습니다."
        self.type = "포인트"
        self.target_id = None
        self.save()

    def get_edit(self, obj):
        self.content = f"{obj.word.title}에 대한 수정 요청이 등록되었습니다."
        self.type = "수정요청"
        self.target_id = obj.id
        self.save()

    def get_question(self, word):
        self.content = f"{word}에 대한 질문이 등록되었습니다."
        self.save()

    def grade_imminent(self, grade):
        self.content = f"{grade}까지 10포인트 남았습니다."
        self.type = "포인트"
        self.target_id = None
        self.save()

    def get_point(self,point):
        self.content = f"{self.user.nickname} 님 {point} 포인트 획득하셨습니다!&#x1F525; (현재 포인트 : {self.user.point}포인트)"
        self.type = "포인트"
        self.target_id = None
        self.save()

    def get_answer(self):
        self.content = f"“나도 궁금해요” 표시한 게시글에 답변이 등록되었습니다"
        self.save()

    def create_word(self,word):
        self.content = f"“등록요청한 단어 {word}가 등록되었습니다."
        self.save()
