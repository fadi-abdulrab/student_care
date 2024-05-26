from email.mime import image
from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=50, default='')
    data =  models.DateField(auto_now=True)
    image = models.URLField( max_length=1000)
    desc = models.TextField()

    def __str__(self):
        return self.title



class class_type(models.Model):
    title = models.CharField(max_length=50, default='')
    data =  models.DateField(auto_now=True)
    image = models.URLField( max_length=1000)
    desc = models.TextField(default='')

    def __str__(self):
        return self.title

