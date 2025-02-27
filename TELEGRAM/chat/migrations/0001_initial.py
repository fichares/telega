# Generated by Django 4.1.7 on 2023-12-20 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat_Application',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('count_participants', models.IntegerField(verbose_name='count participants')),
                ('name_chat', models.CharField(max_length=100, verbose_name='name chat')),
                ('data_time_create', models.DateTimeField(auto_now=True)),
                ('count_message', models.IntegerField(verbose_name='count message')),
                ('creator_chat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
