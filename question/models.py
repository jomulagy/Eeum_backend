from django.db import models

class Question(models.Model):
    author = models.ForeignKey("account.User", on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=300)
    word = models.ForeignKey("word.Word",on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

class Question_Likes(models.Model): #User - Question
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Comment(models.Model): #User - Question
    created_at = models.DateField(auto_now_add=True)
    content = models.CharField(max_length=300, null=False)
    author = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="question_comment", null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)

class Comment_Likes(models.Model): #User - Comment
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE) 
