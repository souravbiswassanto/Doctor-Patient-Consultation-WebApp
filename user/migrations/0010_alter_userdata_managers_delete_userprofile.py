# Generated by Django 4.1.2 on 2023-02-25 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_userprofile'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userdata',
            managers=[
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
