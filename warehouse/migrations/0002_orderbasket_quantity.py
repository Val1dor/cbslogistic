# Generated by Django 2.1.3 on 2018-12-09 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbasket',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
