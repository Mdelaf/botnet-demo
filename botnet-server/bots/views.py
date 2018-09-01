from django.shortcuts import render
from django.views import View

from bots.models import Bot, Task


class BotListView(View):

    def get(self, request):
        bots = Bot.objects.all().order_by('-last_connection')
        tasks = Task.objects.select_related('bot').all().order_by('-created_at')
        return render(request, "botlist.html", context={"bots": bots, "tasks": tasks})


class CommandView(View):

    def post(self, request):
        pass
