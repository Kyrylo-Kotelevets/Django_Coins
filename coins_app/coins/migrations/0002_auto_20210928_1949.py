# Generated by Django 3.2.7 on 2021-09-28 19:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coin',
            options={'ordering': ('-release_date', 'title'), 'verbose_name': 'Coin'},
        ),
        migrations.AddConstraint(
            model_name='coin',
            constraint=models.CheckConstraint(check=models.Q(('release_date__gt', datetime.date(1995, 1, 1))), name='coin_release_date_too_old'),
        ),
    ]