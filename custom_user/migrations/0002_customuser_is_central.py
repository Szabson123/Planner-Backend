# Generated by Django 5.0.7 on 2024-10-28 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_central',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
