from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from bots.models import Bot, Task


class BotListView(View):

    def get(self, request):
        date_from = timezone.now() - timezone.timedelta(minutes=10)
        bots = Bot.objects.filter(last_connection__gte=date_from).order_by('-last_connection')
        tasks = Task.objects.select_related('bot').all().order_by('-created_at')
        return render(request, "botlist.html", context={"bots": bots, "tasks": tasks})


class CommandView(View):

    def post(self, request):
        print(request.POST)
        # TODO: Crear tareas para bots
        pass
