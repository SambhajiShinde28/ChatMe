from django.urls import path
from . import consumers 

websocket_urlpatterns=[
    path('chatme/<str:path>/<str:name>',consumers.ChatMe.as_asgi()),
]