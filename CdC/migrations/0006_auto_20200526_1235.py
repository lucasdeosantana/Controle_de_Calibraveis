# Generated by Django 3.0.6 on 2020-05-26 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CdC', '0005_auto_20200526_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carlog',
            name='destiny',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Destino', to='CdC.Place'),
        ),
        migrations.AlterField(
            model_name='carlog',
            name='origin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Origem', to='CdC.Place'),
        ),
    ]