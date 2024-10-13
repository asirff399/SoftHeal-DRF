from django.db import models
# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    work = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} "


