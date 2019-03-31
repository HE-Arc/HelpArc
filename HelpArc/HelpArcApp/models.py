from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from users.models import Profile
from django.contrib.auth.models import User
# Create your models here.

class Technology(models.Model):
    name = models.CharField(max_length=30)
    logo = models.ImageField()

class SkillLevels(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    technologyId = models.ForeignKey('Technology', on_delete=models.CASCADE, null=True)
    level = models.IntegerField()

class Message(models.Model):
    content = models.TextField()
    date = models.DateField(auto_now=True)
    requestId = models.ForeignKey('Request', on_delete=models.CASCADE, null=True)
    senderId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Request(models.Model):
    title = models.CharField(max_length=50)
    read = models.IntegerField()
    closed = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    studentId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='student')
    helperId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='helper')
    technologyId = models.ForeignKey('Technology', on_delete=models.SET_NULL, null=True)

class Title(models.Model):
    name = models.CharField(max_length=50)

class Class(models.Model):
    name = models.CharField(max_length=10)

