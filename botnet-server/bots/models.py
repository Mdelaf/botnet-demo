from django.db import models
import uuid


class Bot(models.Model):

    uuid = models.CharField(max_length=36)
    os = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    last_connection = models.DateTimeField()


class Task(models.Model):

    uuid = models.CharField(max_length=36, default=uuid.uuid4)
    command = models.CharField(max_length=500)
    total_workers = models.IntegerField()
    workers_running = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Report(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    data = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
