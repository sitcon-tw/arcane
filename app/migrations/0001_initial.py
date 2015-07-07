# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='card',
            fields=[
                ('cid', models.CharField(max_length=16, primary_key=True, serialize=False, default='NfkZ93xhScvuz8gq')),
                ('value', models.IntegerField(default='1', verbose_name='The value of the points card.')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Historicalcard',
            fields=[
                ('cid', models.CharField(db_index=True, max_length=16, default='NfkZ93xhScvuz8gq')),
                ('value', models.IntegerField(default='1', verbose_name='The value of the points card.')),
                ('active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical card',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='Historicalplayer',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('Acquired Points', models.IntegerField(default=0, verbose_name='The amount of points acquired by this player.')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical player',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='Historicalteam',
            fields=[
                ('tid', models.CharField(db_index=True, max_length=32, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('name', models.CharField(null=True, max_length=32)),
                ('Points', models.IntegerField(default=0, verbose_name='The current amount of points of this group.')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical team',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Acquired Points', models.IntegerField(default=0, verbose_name='The amount of points acquired by this player.')),
            ],
        ),
        migrations.CreateModel(
            name='team',
            fields=[
                ('tid', models.CharField(max_length=32, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('name', models.CharField(null=True, max_length=32)),
                ('Points', models.IntegerField(default=0, verbose_name='The current amount of points of this group.')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='app.team'),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalplayer',
            name='team',
            field=models.ForeignKey(null=True, related_name='+', to='app.team', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, blank=True),
        ),
        migrations.AddField(
            model_name='historicalplayer',
            name='user',
            field=models.ForeignKey(null=True, related_name='+', to=settings.AUTH_USER_MODEL, db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, blank=True),
        ),
    ]
