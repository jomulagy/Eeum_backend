from django.db import models

class Message(models.Model):
    content = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    user = models.ForeignKey("account.User",on_delete=models.CASCADE, related_name="messages")

class Request(models.Model):
    content = models.CharField(max_length=100)
    word = models.OneToOneField("word.Word",on_delete=models.SET_NULL, null=True)


