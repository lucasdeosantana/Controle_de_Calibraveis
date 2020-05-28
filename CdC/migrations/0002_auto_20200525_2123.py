# Generated by Django 3.0.6 on 2020-05-26 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CdC', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True, verbose_name='Codigo do Equipamento')),
                ('name', models.CharField(max_length=244, verbose_name='Nome')),
                ('nickName', models.CharField(blank=True, max_length=100, null=True, verbose_name='Apelido')),
                ('where', models.CharField(blank=True, max_length=30, null=True, verbose_name='Localização')),
                ('date_calibration', models.DateField(verbose_name='Data de Calibração')),
                ('validity_time', models.IntegerField(blank=True, null=True, verbose_name='Meses de validade')),
                ('date_validity', models.DateField(blank=True, null=True, verbose_name='Data de validade se preenche automatico se deixado em branco')),
                ('in_calibration', models.IntegerField()),
            ],
            options={
                'permissions': [('can_move', 'Pode mover equipamentos'), ('can_receive', 'Pode receber equipamentos de calibração'), ('can_see_log', 'Pode ver os logs'), ('can_manager_user', 'Pode administrar')],
            },
        ),
        migrations.RenameModel(
            old_name='places',
            new_name='Place',
        ),
        migrations.DeleteModel(
            name='Equipament',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='placa',
            new_name='licensePlate',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='nome',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='position',
            new_name='where',
        ),
        migrations.RenameField(
            model_name='carlog',
            old_name='destino',
            new_name='destiny',
        ),
        migrations.RenameField(
            model_name='carlog',
            old_name='placa',
            new_name='licensePlate',
        ),
        migrations.RenameField(
            model_name='carlog',
            old_name='origem',
            new_name='origin',
        ),
        migrations.RenameField(
            model_name='log',
            old_name='codigo',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='log',
            old_name='destino',
            new_name='destiny',
        ),
        migrations.RenameField(
            model_name='log',
            old_name='origem',
            new_name='origin',
        ),
    ]