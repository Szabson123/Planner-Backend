# Generated by Django 5.0.7 on 2024-10-25 08:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0021_remove_weekendevent_end_time_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='overtime',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['date'], name='plan_event_date_75f038_idx'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['shift'], name='plan_event_shift_i_597f9a_idx'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['user'], name='plan_event_user_id_945a73_idx'),
        ),
    ]
