# Generated by Django 3.0.5 on 2020-04-29 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CdC', '0002_auto_20200429_0433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='observertion',
        ),
        migrations.AlterField(
            model_name='equipament',
            name='date_validity',
            field=models.DateField(blank=True, null=True, verbose_name='Data de validade, se prenche com 1 ano se não informado'),
        ),
    ]
