# Generated by Django 3.0.5 on 2020-04-29 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CdC', '0003_auto_20200429_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='log',
            field=models.ManyToManyField(blank=True, to='CdC.carlog'),
        ),
        migrations.AlterField(
            model_name='equipament',
            name='log',
            field=models.ManyToManyField(blank=True, to='CdC.log'),
        ),
    ]
