# Generated by Django 4.1.2 on 2023-03-13 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_remove_userprofile_otp_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='password',
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='userdata',
            name='user_profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_data', to='user.userprofile'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='NID',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='monthly_income',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='occupation',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
