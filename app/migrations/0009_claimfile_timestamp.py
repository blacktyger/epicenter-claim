# Generated by Django 3.2.2 on 2021-05-12 12:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210512_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimfile',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]