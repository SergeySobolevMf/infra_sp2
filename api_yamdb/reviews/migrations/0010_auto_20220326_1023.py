# Generated by Django 2.2.16 on 2022-03-26 07:23

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('reviews', '0009_auto_20220325_1431'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
    ]
