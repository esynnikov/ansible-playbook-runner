# Generated by Django 2.0.7 on 2018-07-23 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20180722_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]