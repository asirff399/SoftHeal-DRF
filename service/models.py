from django.db import models

# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length = 20)
    description = models.TextField()
    image = models.CharField(max_length=100)

    def __str__(self):
        return self.name