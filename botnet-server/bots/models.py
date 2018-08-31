from django.db import models


# Create your models here.
class Bot(models.Model):

    uuid = models.CharField()
    os = models.CharField()
    username = models.CharField()
    last_connection = models.DateTimeField()


class Task(models.Model):

    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    command = models.CharField()
    answer = models.CharField(blank=True)
