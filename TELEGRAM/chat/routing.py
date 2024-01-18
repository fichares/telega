from django.urls import re_path, path
from chat import consumers



websocket_urlpatterns = [
    re_path(r"ws/chats/(?P<room_name>[^/]+)/$", consumers.ChatConsumer.as_asgi()),
    path('my_chats', consumers.View_last_message_in_chats.as_asgi()),

]
