# Generated by Django 4.1.2 on 2023-03-24 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('response', '0003_response_topic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='response',
            old_name='jon_url',
            new_name='join_url',
        ),
    ]
