# Generated by Django 3.0.5 on 2020-04-30 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CdC', '0010_auto_20200430_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='log',
        ),
        migrations.RemoveField(
            model_name='equipament',
            name='log',
        ),
    ]
