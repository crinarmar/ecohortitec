# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citagro', '0003_auto_20150518_1245'),
    ]

    operations = [
        migrations.CreateModel(
            name='muestra_fenologia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('muestra_a', models.IntegerField(blank=True)),
                ('muestra_b', models.IntegerField(blank=True)),
                ('muestra_c', models.IntegerField(blank=True)),
                ('muestra_d', models.IntegerField(blank=True)),
                ('muestra_e', models.IntegerField(blank=True)),
                ('muestra_f', models.IntegerField(blank=True)),
                ('muestra_g', models.IntegerField(blank=True)),
                ('muestra_h', models.IntegerField(blank=True)),
                ('muestra_i', models.IntegerField(blank=True)),
                ('muestra_j', models.IntegerField(blank=True)),
                ('muestra_k', models.IntegerField(blank=True)),
                ('muestra_l', models.IntegerField(blank=True)),
                ('floracion', models.IntegerField(blank=True)),
                ('idMuestra', models.ForeignKey(related_name='fenologia', to='citagro.Muestreo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='muestra_insetos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coccinelidos', models.IntegerField(blank=True)),
                ('neuropteros', models.IntegerField(blank=True)),
                ('sirfidos', models.IntegerField(blank=True)),
                ('fitoseidos', models.IntegerField(blank=True)),
                ('scutellista', models.IntegerField(blank=True)),
                ('apanteles', models.IntegerField(blank=True)),
                ('aphytis', models.IntegerField(blank=True)),
                ('idMuestra', models.ForeignKey(related_name='insectos', to='citagro.Muestreo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='muestra_trampas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('carpocapsa', models.DecimalField(max_digits=5, decimal_places=3, blank=True)),
                ('idMuestra', models.ForeignKey(related_name='trampas', to='citagro.Muestreo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='muestreo',
            old_name='fecha',
            new_name='fecha_muestreo',
        ),
        migrations.RemoveField(
            model_name='muestreo',
            name='detalles',
        ),
        migrations.RemoveField(
            model_name='muestreo',
            name='horas',
        ),
        migrations.AddField(
            model_name='muestreo',
            name='idExplotacion',
            field=models.ForeignKey(related_name='muestrasExplotacion', default=1, to='citagro.Explotacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='muestreo',
            name='observaciones',
            field=models.TextField(default='Sin observaciones', blank=True),
            preserve_default=False,
        ),
    ]
