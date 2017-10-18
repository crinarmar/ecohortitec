# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citagro', '0006_auto_20150522_1118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='muestra_fenologia',
            old_name='floracion',
            new_name='muestra_a1',
        ),
        migrations.RenameField(
            model_name='muestra_fenologia',
            old_name='muestra_g',
            new_name='muestra_a2',
        ),
        migrations.RenameField(
            model_name='muestra_fenologia',
            old_name='muestra_h',
            new_name='muestra_a3',
        ),
        migrations.RenameField(
            model_name='muestra_fenologia',
            old_name='muestra_i',
            new_name='muestra_e1',
        ),
        migrations.RenameField(
            model_name='muestra_fenologia',
            old_name='muestra_j',
            new_name='muestra_e2',
        ),
        migrations.RenameField(
            model_name='muestra_fenologia',
            old_name='muestra_k',
            new_name='muestra_e3',
        ),
        migrations.RenameField(
            model_name='muestra_fenologia',
            old_name='muestra_l',
            new_name='muestra_f1',
        ),
    ]
