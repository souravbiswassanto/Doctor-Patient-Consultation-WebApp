# Generated by Django 4.1.2 on 2023-03-13 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_remove_userdata_rating'),
        ('doctor', '0005_doctordata_activetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctordata',
            name='activetime',
        ),
        migrations.RemoveField(
            model_name='doctordata',
            name='phonenumber',
        ),
        migrations.AddField(
            model_name='doctordata',
            name='user_profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_data', to='user.userprofile'),
        ),
    ]
