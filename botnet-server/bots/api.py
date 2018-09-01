from django.utils.decorators import method_decorator
from django.views import View
from bots.auth import bot_authentication


class AuthView(View):

    def post(self, request):
        pass


class TaskView(View):

    @method_decorator(bot_authentication)
    def get(self, request):
        pass


class DeliveryView(View):

    @method_decorator(bot_authentication)
    def post(self, request):
        pass


