# Generated by Django 3.0.5 on 2020-05-01 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CdC', '0015_auto_20200430_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='in_use',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Utilizador'),
        ),
    ]
