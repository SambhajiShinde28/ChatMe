# Generated by Django 5.0.6 on 2024-08-17 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels_testing', '0006_remove_newgroupsmodel_group_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='newgroupsmodel',
            name='Unique_Id',
            field=models.TextField(default=123),
            preserve_default=False,
        ),
    ]
