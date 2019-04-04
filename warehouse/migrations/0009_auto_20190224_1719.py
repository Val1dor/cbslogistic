# Generated by Django 2.1.3 on 2019-02-24 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_auto_20190224_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderbasket',
            old_name='discount',
            new_name='discount_abs',
        ),
        migrations.AddField(
            model_name='orderbasket',
            name='discount_percent',
            field=models.IntegerField(default=0),
        ),
    ]