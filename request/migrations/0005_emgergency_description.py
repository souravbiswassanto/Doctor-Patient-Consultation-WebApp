# Generated by Django 4.1.2 on 2023-03-20 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0004_remove_emgergency_doctor_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emgergency',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
