# Generated by Django 2.2.12 on 2020-04-03 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0012_aggregation_and_threshold_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='description',
            field=models.TextField(default=''),
        ),
    ]