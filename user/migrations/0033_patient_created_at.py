# Generated by Django 4.1.2 on 2023-03-22 08:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0032_alter_patient_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 22, 8, 0, 44, 114171, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
