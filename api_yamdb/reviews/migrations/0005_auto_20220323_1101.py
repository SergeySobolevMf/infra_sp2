# Generated by Django 2.2.16 on 2022-03-23 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220323_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews_title', to='reviews.Title'),
        ),
    ]