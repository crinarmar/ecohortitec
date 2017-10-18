# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecologica', '0002_auto_20151203_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repositorioimagenes',
            name='imagen',
            field=models.ImageField(upload_to=b''),
        ),
    ]
