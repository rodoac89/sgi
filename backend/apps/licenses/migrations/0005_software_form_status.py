# Generated by Django 3.2 on 2021-10-22 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenses', '0004_alter_licenses_list_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='SoftwareForm',
            name='status',
            field=models.IntegerField(choices=[(1, 'No realizada'), (2, 'Realizada')], default=1),
        ),
    ]