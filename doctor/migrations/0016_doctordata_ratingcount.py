# Generated by Django 4.1.2 on 2023-03-29 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0015_alter_doctordata_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctordata',
            name='ratingcount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
