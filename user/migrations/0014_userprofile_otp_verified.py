# Generated by Django 4.1.2 on 2023-02-27 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_userprofile_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='otp_verified',
            field=models.BooleanField(default=False),
        ),
    ]
