from django.db import models

class Vocabulary(models.Model):
    user = models.ForeignKey("account.User",on_delete = models.CASCADE)
    word = models.ForeignKey("word.Word",on_delete=models.CASCADE)

