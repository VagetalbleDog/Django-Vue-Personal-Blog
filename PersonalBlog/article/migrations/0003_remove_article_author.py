# Generated by Django 3.1.3 on 2022-01-05 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
    ]
