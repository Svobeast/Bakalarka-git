from django.db import models

# Create your models here.
class Numbers(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()
