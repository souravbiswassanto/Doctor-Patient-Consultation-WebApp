# Generated by Django 4.1.2 on 2023-03-25 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0040_alter_patient_created_at'),
        ('response', '0005_alter_response_doctorack'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientid', models.IntegerField(blank=True, null=True)),
                ('meetingid', models.IntegerField(blank=True, null=True)),
                ('uploaded_by', models.CharField(blank=True, max_length=10, null=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('filename', models.CharField(blank=True, max_length=100, null=True)),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_data_file', to='user.userprofile')),
            ],
        ),
    ]