from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class AdminPanel(admin.ModelAdmin):
    list_display = ["username", "id", "profile_picture", "DataCreateUser", "img_preview", "online"]
    list_filter = ('username', 'data_birn', 'DataCreateUser')
    readonly_fields = ['img_preview']

    class Meta:
        model = User




admin.site.register(User, AdminPanel)