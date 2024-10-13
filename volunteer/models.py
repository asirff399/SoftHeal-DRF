from django.db import models
from .constants import GENDER_TYPE_CHOICES,BRANCH_TYPE_CHOICES
# Create your models here.

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.DecimalField(max_digits=11, decimal_places=0)
    gender = models.CharField(max_length=30, choices=GENDER_TYPE_CHOICES ,default='Male')
    branch = models.CharField(max_length=30, choices=BRANCH_TYPE_CHOICES ,default='Rajshahi')
    image = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} "
