# Generated by Django 2.2.12 on 2020-04-03 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem_super_admin', '0020_metrictemplate_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='metrictemplatehistory',
            name='description',
            field=models.TextField(default=''),
        ),
    ]