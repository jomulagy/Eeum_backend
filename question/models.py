from django.db import models
from word.models import Word
from account.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    word = models.OneToOneField(Word,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    views = models.IntegerField()
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

class likes: #User - Question
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Request_id = models.ForeignKey(Question, on_delete=models.CASCADE)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    read = models.BooleanField(default=False)

class Comment(models.Model): #User - Question
    created_at = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.ForeignKey(Question, on_delete=models.CASCADE)

class likes2(models.Model): #User - Comment
    Request_id = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.ForeignKey(Comment, on_delete=models.CASCADE)

class likes3(models.Model): #User - Words
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Word_id = models.ForeignKey(Word, on_delete=models.CASCADE)

class likes4(models.Model): #User - Comment
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)