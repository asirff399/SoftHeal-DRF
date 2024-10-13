from django.db import models
from django.contrib.auth.models import User
# from cloudinary.models import CloudinaryField
# Create your models here.

class PostType(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)

    def __str__(self):
        return self.name

class Post(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=200)    
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    target = models.IntegerField()
    collected = models.IntegerField(default=0)
    post_type = models.ForeignKey(PostType,on_delete=models.CASCADE) 


class Donation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    donated_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    balance_after_donation = models.IntegerField()

    def __str__(self):
        return f"{self.post.name} donated By {self.user.username}"

