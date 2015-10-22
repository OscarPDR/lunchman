# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendedMeal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('preferred_time', models.CharField(default=b'ordinary', max_length=15, choices=[(b'ordinary', b'Subo a las 13h'), (b'delayed', b'Subo m\xc3\xa1s tarde, esperad'), (b'non-attending', b'No subo')])),
                ('person', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dessert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meal', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='FirstCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meal', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='MealTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remaining_meals', models.PositiveSmallIntegerField(default=20)),
                ('purchased', models.DateField(auto_now_add=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(unique=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='SecondCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meal', models.CharField(max_length=75)),
                ('menu', models.ForeignKey(to='website.Menu')),
            ],
        ),
        migrations.AddField(
            model_name='firstcourse',
            name='menu',
            field=models.ForeignKey(to='website.Menu'),
        ),
        migrations.AddField(
            model_name='dessert',
            name='menu',
            field=models.ForeignKey(to='website.Menu'),
        ),
        migrations.AlterUniqueTogether(
            name='mealticket',
            unique_together=set([('owner', 'purchased')]),
        ),
        migrations.AlterUniqueTogether(
            name='attendedmeal',
            unique_together=set([('person', 'date')]),
        ),
    ]
