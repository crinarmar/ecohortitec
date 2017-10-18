# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citagro', '0005_muestreo_horas'),
    ]

    operations = [
        migrations.CreateModel(
            name='muestra_brotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('carpocapsa', models.IntegerField(blank=True)),
                ('acaros', models.IntegerField(blank=True)),
                ('pulgones', models.IntegerField(blank=True)),
                ('idMuestra', models.ForeignKey(related_name='brotes', to='citagro.Muestreo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='muestra_enfermedades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bacteriosis', models.IntegerField(blank=True)),
                ('antracnosis', models.IntegerField(blank=True)),
                ('idMuestra', models.ForeignKey(related_name='enfermedades', to='citagro.Muestreo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='muestra_zeuzera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zeuzera', models.IntegerField(blank=True)),
                ('idMuestra', models.ForeignKey(related_name='zeuzera', to='citagro.Muestreo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='muestreo',
            name='idUHC',
            field=models.ForeignKey(related_name='muestreo', to='citagro.UHC'),
            preserve_default=True,
        ),
    ]
