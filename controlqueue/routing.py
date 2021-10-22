from django.urls import path

from . import consumers
from .apps import ControlqueueConfig

app_name = ControlqueueConfig.name

websocket_urlpatterns = [
	path('ws/queue/<str:group_name>/', consumers.QueueConsumer.as_asgi(), name='queue_group'),
]
