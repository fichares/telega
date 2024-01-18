import uuid

from django.db import models

from user_app.models import User


class Chat_Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False, unique=True)
    count_participants = models.IntegerField('count participants')
    name_chat = models.CharField('name chat', max_length=100)
    creator_chat = models.ForeignKey(User, on_delete=models.PROTECT)
    data_time_create = models.DateTimeField(auto_now=True)
    count_message = models.IntegerField('count message')
    picture = models.ImageField("chat's avatarka", default="default_pictrute-chat.png", upload_to="static/chat/images/avatarki_chat/")
    slug = models.SlugField(default="test")

    def save(self, *args, **kwargs):
        from django.template.defaultfilters import slugify
        self.slug = slugify(self.name_chat)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_chat

class Users_Chat(models.Model):
    users = models.ForeignKey(User, on_delete=models.PROTECT)
    chat = models.ForeignKey(Chat_Application, on_delete=models.PROTECT)

class MessageUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False, unique=True)
    text = models.CharField('text message', max_length=400)
    users_send = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_it_is = models.ForeignKey(Chat_Application, on_delete=models.CASCADE)
    data_create = models.DateTimeField(auto_now=True)
    status_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.chat_it_is ) + ' ' + str(self.text)


