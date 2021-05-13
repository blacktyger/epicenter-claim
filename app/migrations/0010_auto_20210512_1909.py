# Generated by Django 3.2.2 on 2021-05-12 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_claimfile_timestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='claim',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='claimfile',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterField(
            model_name='claim',
            name='details',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='claim',
            name='team_comments',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='claim',
            name='vitex_address',
            field=models.CharField(blank=True, default='', max_length=56, null=True),
        ),
    ]
