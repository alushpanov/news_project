# Generated by Django 3.1.7 on 2021-03-12 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', 'MtoM_rel_moved_to_Article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='articles', to='news.Category'),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name=''),
        ),
    ]
