from django.db import models

class Word(models.Model):

    likes = models.ManyToManyField("account.User",related_name = "like_words",null = True)

    def get_likes(self):
        return self.likes.all().count()
