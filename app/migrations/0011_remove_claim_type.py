# Generated by Django 3.2.2 on 2021-05-12 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210512_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='type',
        ),
    ]
