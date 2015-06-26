# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserVerification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, db_index=True)),
                ('validation_key', models.IntegerField(db_index=True)),
            ],
        ),
        migrations.AlterIndexTogether(
            name='userverification',
            index_together=set([('email', 'validation_key')]),
        ),
    ]
