# Generated by Django 4.1.2 on 2023-02-19 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_patient_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='rating',
            field=models.FloatField(null=True),
        ),
    ]
