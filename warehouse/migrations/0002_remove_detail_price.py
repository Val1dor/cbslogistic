# Generated by Django 2.1.3 on 2019-04-04 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detail',
            name='price',
        ),
    ]
