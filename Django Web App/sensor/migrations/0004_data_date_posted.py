# Generated by Django 2.2 on 2019-04-17 04:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0003_auto_20190415_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
