from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Word(models.Model):
    title = models.IntegerField(max_length= 16)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField(max_length = 8)

    likes = models.ManyToManyField("account.User",related_name = "like_word",null = True)

    def get_likes(self):
        return self.likes.all().count()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=32)
    image = models.ImageField(null=True,blank=True,upload_to="" )
    views= models.IntegerField(max_length=8)


class Edit(models.Model):
    title = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    views= models.IntegerField(max_length=8)
    content = models.TextField(max_length=32)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    likes = models.ManyToManyField("account.User",related_name = "like_edit",null = True)

    def get_likes(self):
        return self.likes.all().count()



class Comment(models.Model): #do
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=32)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    edit = models.ForeignKey(Edit, on_delete=models.CASCADE)
    likes = models.ManyToManyField("account.User",related_name = "like_comment",null = True)

    def get_likes(self):
        return self.likes.all().count()

class Vocabulary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    words = models.ManyToManyField('Word')
