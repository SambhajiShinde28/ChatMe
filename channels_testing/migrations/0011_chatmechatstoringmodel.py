# Generated by Django 5.0.6 on 2024-08-21 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels_testing', '0010_remove_newgroupsmodel_channel_layer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMeChatStoringModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Unique_Id', models.TextField()),
                ('Groups_Name', models.TextField()),
                ('Person_Name', models.TextField()),
                ('ChatMe_Message', models.TextField()),
                ('Message_Sequence', models.TextField()),
            ],
        ),
    ]