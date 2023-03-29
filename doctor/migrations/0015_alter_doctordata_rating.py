# Generated by Django 4.1.2 on 2023-03-29 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0014_doctordata_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctordata',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=2, null=True),
        ),
    ]
