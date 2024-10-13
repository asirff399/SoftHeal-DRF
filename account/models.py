from django.db import models
from django.contrib.auth.models import User
from .constants import STAR_CHOICES,USER_TYPE_CHOICES

# Create your models here.

class CustomUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    image = models.CharField(max_length=200) 
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    phone = models.DecimalField(default=0, max_digits=11, decimal_places=0)
    address = models.CharField(max_length=200)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES,default='User')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Review(models.Model):
    reviewer = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    # post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=20,choices=STAR_CHOICES)

    def __str__(self):
        return f"Reviewer: {self.reviewer.user.first_name}; Pet: {self.pet.name}"

    