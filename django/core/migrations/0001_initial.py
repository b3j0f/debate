# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 13:53
from __future__ import unicode_literals

import address.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='address.Address')),
            ],
        ),
        migrations.CreateModel(
            name='CommentedElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ForbiddenEmail',
            fields=[
                ('email', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=b'')),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectionEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(db_index=True, max_length=255)),
                ('answers', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('date', models.DateField(default=datetime.date.today, primary_key=True, serialize=False)),
                ('accounts', models.IntegerField(default=0)),
                ('topics', models.IntegerField(default=0)),
                ('spaces', models.IntegerField(default=0)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('account', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='core.Account')),
            ],
        ),
        migrations.CreateModel(
            name='AdministratedElement',
            fields=[
                ('commentedelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.CommentedElement')),
                ('name', models.CharField(blank=True, db_index=True, max_length=50)),
                ('description', models.CharField(blank=True, db_index=True, max_length=255)),
                ('public', models.BooleanField(db_index=True, default=True)),
            ],
            bases=('core.commentedelement',),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentedelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.CommentedElement')),
                ('content', models.CharField(db_index=True, max_length=255)),
            ],
            bases=('core.commentedelement',),
        ),
        migrations.AddField(
            model_name='vote',
            name='voted',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='core.CommentedElement'),
        ),
        migrations.AddField(
            model_name='media',
            name='source',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='core.CommentedElement'),
        ),
        migrations.AddField(
            model_name='commentedelement',
            name='tags',
            field=models.ManyToManyField(blank=True, default=[], related_name='tagged', to='core.Tag'),
        ),
        migrations.AddField(
            model_name='account',
            name='avatar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Media'),
        ),
        migrations.AddField(
            model_name='account',
            name='languages',
            field=models.ManyToManyField(blank=True, default=[], related_name='_account_languages_+', to='address.Country'),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('date', models.DateField(blank=True, db_index=True)),
                ('mduration', models.IntegerField(blank=True, db_index=True, default=60)),
                ('base', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_event', serialize=False, to='core.AdministratedElement')),
            ],
            bases=('core.administratedelement',),
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('lon', models.FloatField(blank=True, db_index=True)),
                ('lat', models.FloatField(blank=True, db_index=True)),
                ('base', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_space', serialize=False, to='core.AdministratedElement')),
                ('address', address.models.AddressField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='address.Address')),
            ],
            bases=('core.administratedelement',),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('base', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='_topic', serialize=False, to='core.AdministratedElement')),
            ],
            bases=('core.administratedelement',),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('account', 'voted')]),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.Account'),
        ),
        migrations.AddField(
            model_name='comment',
            name='cited',
            field=models.ManyToManyField(blank=True, default=[], related_name='cited', to='core.Account'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commentated',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.CommentedElement'),
        ),
        migrations.AddField(
            model_name='administratedelement',
            name='admins',
            field=models.ManyToManyField(blank=True, default=[], related_name='administrated', to='core.Account'),
        ),
        migrations.AddField(
            model_name='projectionentry',
            name='event',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.Event'),
        ),
        migrations.AddField(
            model_name='event',
            name='space',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='core.Space'),
        ),
        migrations.AddField(
            model_name='event',
            name='topic',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='core.Topic'),
        ),
    ]
