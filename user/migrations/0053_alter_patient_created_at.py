# Generated by Django 4.1.2 on 2023-03-28 22:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0052_userdata_is_sub_alter_patient_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 28, 22, 56, 2, 434710, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
