# Generated by Django 3.1.7 on 2021-03-16 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', 'datetime_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
