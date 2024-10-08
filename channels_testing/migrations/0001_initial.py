# Generated by Django 5.0.6 on 2024-07-04 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupsName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupnames', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='ChatModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.CharField(max_length=100000000)),
                ('grops', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channels_testing.groupsname')),
            ],
        ),
    ]
