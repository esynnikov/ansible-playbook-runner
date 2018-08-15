# Generated by Django 2.0.7 on 2018-07-26 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_buildset_buildsetitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildset',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buildset',
            name='name',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buildset',
            name='projectid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buildsetitems',
            name='buildsetid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buildsetitems',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buildsetitems',
            name='playbookid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buildsetitems',
            name='projectid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]