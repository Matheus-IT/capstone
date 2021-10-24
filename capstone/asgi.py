# --------------------- Has to come before anything else ---------------------
from django.core.asgi import get_asgi_application

get_asgi_app = get_asgi_application()
# ----------------------------------------------------------------------------

import os
import django
import controlqueue.routing

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capstone.settings')
django.setup()

application = ProtocolTypeRouter(
    {
        'http': get_asgi_app,
        'websocket': AuthMiddlewareStack(
            URLRouter(controlqueue.routing.websocket_urlpatterns)
        ),
    }
)
