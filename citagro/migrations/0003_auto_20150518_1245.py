# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citagro', '0002_tecnico_activo'),
    ]

    operations = [
        migrations.AddField(
            model_name='aplicador',
            name='activo',
            field=models.CharField(default=b'SI', max_length=2, choices=[(b'SI', b'Si'), (b'NO', b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maquinaria',
            name='activo',
            field=models.CharField(default=b'SI', max_length=2, choices=[(b'SI', b'Si'), (b'NO', b'No')]),
            preserve_default=True,
        ),
    ]
