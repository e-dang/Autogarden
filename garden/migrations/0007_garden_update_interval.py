# Generated by Django 3.1.6 on 2021-02-25 21:32

from django.db import migrations, models
import garden.models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0006_garden_last_connection_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='garden',
            name='update_interval',
            field=models.DurationField(default=garden.models._default_update_interval),
        ),
    ]
