from django.contrib import admin

from chat.models import Chat_Application, MessageUser, Users_Chat

admin.site.register(Chat_Application)
admin.site.register(Users_Chat)
admin.site.register(MessageUser)
