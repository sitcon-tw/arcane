# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('cid', models.CharField(verbose_name='Card ID', serialize=False, default='dibBDvxA25b08TcD', max_length=16, help_text='The unique ID for the points card.', primary_key=True)),
                ('value', models.IntegerField(default='1', help_text='The value of the points card.', verbose_name='Value')),
                ('active', models.BooleanField(default=True, verbose_name='Active?')),
                ('retrieved', models.BooleanField(default=False, verbose_name='Retrieved')),
                ('name', models.CharField(max_length=32, help_text='Name of the card.', blank=True, verbose_name='Name')),
                ('long_desc', models.TextField(help_text='Long descriptions about the card.', blank=True, verbose_name='Descriptions')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('no', models.AutoField(serialize=False, primary_key=True)),
                ('action', models.IntegerField(choices=[(1, '建立卡片'), (2, '編輯卡片'), (3, '關閉卡片'), (4, '啟動卡片'), (10, '獲得卡片')])),
                ('comment', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('card', models.ForeignKey(to='app.Card')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('tid', models.CharField(max_length=32, help_text='Alphanumeric name for the team.', serialize=False, verbose_name='Team ID', primary_key=True)),
                ('name', models.CharField(max_length=100, help_text='Name of the team.', verbose_name='Name')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='app.Team', help_text='The team this player belongs to.', verbose_name='Team', related_name='player'),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, help_text='The user of this player.', verbose_name='User'),
        ),
        migrations.AddField(
            model_name='card',
            name='capturer',
            field=models.ForeignKey(to='app.Player', blank=True, null=True, related_name='captured_card'),
        ),
        migrations.AddField(
            model_name='card',
            name='issuer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='issued_card'),
        ),
    ]
