from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from bots.models import Bot, Task, Report


class IndexView(View):

    def get(self, request):
        date_from = timezone.now() - timezone.timedelta(minutes=10)
        bots = Bot.objects.filter(last_connection__gte=date_from).order_by('-last_connection')
        tasks = Task.objects.all().order_by('-created_at')
        reports = Report.objects.all().select_related('bot', 'task').order_by('-created_at')
        return render(request, "botlist.html", context={"bots": bots, "tasks": tasks, "reports": reports})


class CommandView(View):

    def post(self, request):
        name = request.POST.get("name")
        bots = request.POST.get("bots")

        length = request.POST.get("length")
        url = request.POST.get("url")
        charset = request.POST.get("charset")
        hashing_algorithm = request.POST.get("hashing-algorithm")

        if all([name, bots, length, url, charset, hashing_algorithm]):
            command = "bruteforce -u {} -a {} -s {} -l {}".format(url, hashing_algorithm, charset, length)
            Task.objects.create(name=name, command=command, total_workers=bots)

        return redirect("index")

