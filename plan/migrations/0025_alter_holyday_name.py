# Generated by Django 5.0.7 on 2024-10-25 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0024_holyday_delete_hourdaycounter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holyday',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
