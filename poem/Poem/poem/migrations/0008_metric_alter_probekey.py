# Generated by Django 2.2.5 on 2019-12-04 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poem_super_admin', '0005_probehistory'),
        ('poem', '0007_userprofile_groupsofthresholdsprofiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metric',
            name='probekey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='poem_super_admin.ProbeHistory'),
        ),
    ]
