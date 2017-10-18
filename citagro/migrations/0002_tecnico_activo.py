# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citagro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tecnico',
            name='activo',
            field=models.CharField(default=b'SI', max_length=2, choices=[(b'SI', b'Si'), (b'NO', b'No')]),
            preserve_default=True,
        ),
    ]
