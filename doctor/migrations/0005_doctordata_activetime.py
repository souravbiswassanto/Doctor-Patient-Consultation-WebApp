# Generated by Django 4.1.2 on 2023-02-21 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_blockeduser_spamreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctordata',
            name='activetime',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
