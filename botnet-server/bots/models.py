from django.db import models


# Create your models here.
class Bot(models.Model):

    uuid = models.CharField(max_length=36)
    os = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    last_connection = models.DateTimeField()


class Task(models.Model):

    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    command = models.CharField(max_length=500)
    answer = models.CharField(blank=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
