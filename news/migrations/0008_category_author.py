# Generated by Django 3.1.7 on 2021-04-13 06:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from my_auth.models import MyUser


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0007_comments_related_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='author',
            field=models.ForeignKey(default=MyUser.objects.get(is_staff=True).id, on_delete=django.db.models.deletion.CASCADE, to='my_auth.myuser'),
            preserve_default=False,
        ),
    ]
