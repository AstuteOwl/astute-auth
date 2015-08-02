# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserClaim',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, db_index=True)),
                ('claim_name', models.CharField(max_length=50, db_index=True)),
                ('claim_value', models.CharField(max_length=254)),
            ],
        ),
        migrations.AlterIndexTogether(
            name='userclaim',
            index_together=set([('email', 'claim_name')]),
        ),
    ]
