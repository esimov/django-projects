# Generated by Django 2.2.5 on 2019-10-11 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_auto_20191009_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.TextField(max_length=4000),
        ),
    ]
