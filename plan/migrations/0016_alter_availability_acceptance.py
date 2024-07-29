# Generated by Django 5.0.7 on 2024-07-29 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0015_availability_freeday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='acceptance',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
