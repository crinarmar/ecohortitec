# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecologica', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expediente',
            name='indProdParalela',
            field=models.CharField(default=b'NP', max_length=2, choices=[(b'SI', b'Si'), (b'NO', b'No'), (b'NP', b'NP')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ganado',
            name='animales',
            field=models.CharField(default=b'0', max_length=6),
            preserve_default=True,
        ),
    ]
