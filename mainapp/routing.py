from django.urls import path
from mainapp.consumers import AsgiConsumer

websocket_urlpatterns = [
    path("ws/asgi/", AsgiConsumer.as_asgi()),
]
