# Generated by Django 3.2.7 on 2021-10-19 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='relevant_tokens',
        ),
    ]
