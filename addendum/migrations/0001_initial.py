# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('key', models.CharField(max_length=250, serialize=False, primary_key=True)),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ('key',),
            },
            bases=(models.Model,),
        ),
    ]
