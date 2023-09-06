# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-12-20 11:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sss', '0002_auto_20171013_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='mobile_image',
            field=models.ImageField(blank=True, help_text='Deze afbeelding wordt de banner van deze pagina op de smalste layout. Als je hier géén afbeelding kiest, dan wordt de afbeelding desktop gebruikt, maar wel verkleind tot een breedte van 800 pixels.', upload_to='', verbose_name='afbeelding (mobiel)'),
        ),
    ]
