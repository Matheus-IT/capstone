from django.urls import path

from .apps import MysiteConfig
from . import views

app_name = MysiteConfig.name

urlpatterns = [
	path('', views.index, name='index'),
	path('waitingQueue/', views.waiting_queue, name='waiting_queue')
]
