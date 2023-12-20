import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe



Push_Category = (
    ("1", "news"),
    ("2", "reminders"),
)

class User(AbstractUser):
    first_name = models.CharField("person's first name", max_length=70, editable=True)
    last_name = models.CharField("person's last name", max_length=70,editable=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField("person's username", max_length=70, editable=True, unique=True)
    email = models.EmailField("person's email", max_length=70, editable=True, unique=True)
    password = models.CharField("person's password", max_length=400)
    profile_picture =  models.ImageField("person's avatarka", default="avatarka_default.png", upload_to="static/user_app/images/avatarki/")
    quotation = models.CharField("person's quotation", max_length=150, editable=True)
    data_birn = models.DateField("person's data birn", default="2000-1-1")
    DataCreateUser = models.DateField("person's data create account", auto_now=True, editable=False)
    online = models.BooleanField("person's online", default=True)
    def __str__(self):
        return self.username

    def img_preview(self):  # new
        return mark_safe(f'<img src = "{self.profile_picture.url}" width = "30"/>')


class PushNotif(models.Model):
    id = models.UUIDField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField("title push", max_length=70, editable=True)
    body = models.CharField("title push", max_length=70, editable=True)
    data_create = models.DateTimeField("create push", auto_now=True, editable=False)
    read = models.BooleanField(default=False)
    category = models.CharField(choices=Push_Category, max_length=60)






