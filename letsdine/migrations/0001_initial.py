# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-02 01:28
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Intrest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=400)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('going_time', models.DateTimeField()),
                ('food_type', models.CharField(choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg'), ('Both', 'Both')], max_length=20)),
                ('place', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('other_users', models.ManyToManyField(blank=True, related_name='iplans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plan_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('A', 'Accepted'), ('R', 'Rejected'), ('P', 'Pending')], default='P', max_length=1)),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='letsdine.Plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_pic', models.ImageField(blank=True, default='pic_folder/user.jpg', null=True, upload_to='pic_folder/')),
                ('contact_no', models.BigIntegerField(blank=True, default=0)),
                ('city_name', models.CharField(blank=True, max_length=40)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=20)),
                ('age', models.IntegerField(blank=True, default=18)),
                ('occupation', models.CharField(blank=True, max_length=40)),
                ('about_you', models.CharField(blank=True, max_length=500)),
                ('fb_link', models.URLField(blank=True, max_length=100)),
                ('twitter_link', models.URLField(blank=True, max_length=100)),
                ('insta_link', models.URLField(blank=True, max_length=100)),
                ('intrests', models.ManyToManyField(blank=True, to='letsdine.Intrest')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letsdine.Plan'),
        ),
    ]