# Generated by Django 2.0.7 on 2018-07-20 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_playtree_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playtree',
            name='parent',
        ),
    ]
