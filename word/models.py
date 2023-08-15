from django.db import models

class Age(models.Model):
    value = models.IntegerField()


class Word(models.Model):
    title = models.CharField(max_length= 16)
    author = models.ForeignKey("account.User", on_delete=models.CASCADE, null=True)
    age = models.ManyToManyField(Age)
    mean = models.CharField(max_length=40)
    content = models.TextField(max_length=300, default='')
    image = models.ImageField(upload_to="word", null=True)
    likes = models.ManyToManyField("account.User",related_name = "like_word")
    def get_likes(self):
        return self.likes.all().count()
    created_at = models.DateTimeField(auto_now_add = True, blank=True)
    views= models.IntegerField(default=0)
    best = models.BooleanField(default=False)


class Edit(models.Model):
    word = models.ForeignKey("word.Word", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=300)
    author = models.ForeignKey("account.User", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField("account.User", related_name = "like_edit")
    def get_likes(self):
        return self.likes.all().count()
    views= models.IntegerField(default=0)


class Comment(models.Model): #단어 comment 이게 수정요청이니?
    edit = models.ForeignKey("word.Edit", on_delete=models.CASCADE, null=True)

    content = models.TextField(max_length=300)

    author = models.ForeignKey("account.User", on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField("account.User",related_name = "like_comment")
    def get_likes(self):
        return self.likes.all().count()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    views= models.IntegerField(default=0)
