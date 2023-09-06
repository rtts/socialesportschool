# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-13 14:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootcamps', '0003_auto_20170927_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bootcamp',
            name='places',
            field=models.PositiveIntegerField(default=10, verbose_name='beschikbare plaatsen'),
        ),
        migrations.AlterField(
            model_name='sportschool',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='Geef hier de account op die deze sportschool mogen beheren', related_name='sportscholen', to=settings.AUTH_USER_MODEL, verbose_name='Gebruikers'),
        ),
        migrations.AlterField(
            model_name='zorglocatie',
            name='sportscholen',
            field=models.ManyToManyField(blank=True, help_text='Selecter hier de sportclubs waarmee deze zorglocatie samenwerkt', related_name='zorglocaties', to='bootcamps.Sportschool', verbose_name='Samenwerking met'),
        ),
        migrations.AlterField(
            model_name='zorglocatie',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='Geef hier de accounts op die deze zorglocatie mogen beheren', related_name='zorglocaties', to=settings.AUTH_USER_MODEL, verbose_name='Gebruikers'),
        ),
    ]
