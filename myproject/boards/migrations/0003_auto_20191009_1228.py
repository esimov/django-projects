# Generated by Django 2.2.5 on 2019-10-09 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_topic_view'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='view',
            new_name='views',
        ),
    ]
