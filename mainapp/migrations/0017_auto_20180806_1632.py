# Generated by Django 2.0.7 on 2018-08-06 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_build_currentplay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='currentplay',
            field=models.IntegerField(),
        ),
    ]