# Generated by Django 4.1.2 on 2023-03-14 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_userdata_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='confirmpassword',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='newpassword',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='oldpassword',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
