from django.db import models

class Word(models.Model):
    title = models.IntegerField(max_length= 16)
    author = models.ForeignKey("account.User", on_delete=models.CASCADE)
    age = models.IntegerField(max_length = 8)

    likes = models.ManyToManyField("account.User",related_name = "like_word",null = True)

    def get_likes(self):
        return self.likes.all().count()

    created_at = models.DateTimeField(default=timezone.now, blank=True)
    content = models.TextField(max_length=32, default='')
    # image = models.ImageField(upload_to="" )
    views= models.IntegerField(default='0')



class Comment(models.Model): #단어 comment 이게 수정요청이니?
    created_at = models.DateTimeField(auto_now_add=True)
    views= models.IntegerField(max_length=8)
    content = models.TextField(max_length=32)
    author = models.ForeignKey("account.User", on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    likes = models.ManyToManyField("account.User",related_name = "like_edit",null = True)

    def get_likes(self):
        return self.likes.all().count()


# class Edit(models.Model):
#     title = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     views= models.IntegerField(max_length=8)
#     content = models.TextField(max_length=32)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     word = models.ForeignKey(Word, on_delete=models.CASCADE)
#     likes = models.ManyToManyField("account.User",related_name = "like_edit",null = True)

class Comment(models.Model): #do
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=32)
    author = models.ForeignKey("account.User", on_delete=models.CASCADE)
    edit = models.ForeignKey(Edit, on_delete=models.CASCADE)
    likes = models.ManyToManyField("account.User",related_name = "like_comment",null = True)

    def get_likes(self):
        return self.likes.all().count()

