# Generated by Django 2.2.1 on 2019-06-12 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sss', '0003_auto_20181220_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='external_url',
            field=models.URLField(blank=True, verbose_name='externe URL'),
        ),
    ]
