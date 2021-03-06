from django.utils import timezone

from bots.models import Bot
from django.http import HttpResponse


def bot_authentication(func):
    def __bot_authentication(request, *args, **kwargs):
        authorization = request.META.get("HTTP_AUTHORIZATION", "")
        authorization_split = authorization.split()
        if len(authorization_split) == 2 and authorization_split[0] == "Token":
            uuid = authorization_split[1]
            bot = Bot.objects.filter(uuid=uuid).first()
            if bot:
                bot.last_connection = timezone.now()
                bot.save()
                request.bot = bot
                return func(request, *args, **kwargs)
        return HttpResponse(status=401)
    return __bot_authentication
