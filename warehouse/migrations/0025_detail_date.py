# Generated by Django 2.1.3 on 2019-03-31 08:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0024_auto_20190303_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
