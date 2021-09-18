from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    username = models.TextField(max_length=50)
    followers = models.IntegerField()
    lastUpdated = models.DateTimeField(auto_now_add=True)
    user = OneToOneField(User, on_delete=models.CASCADE)
    

class Repository(models.Model):
    name = models.TextField(max_length=50)
    stars = models.IntegerField()
    profile = ForeignKey(Profile, on_delete=models.CASCADE)