# Generated by Django 3.2.4 on 2021-10-31 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_workstation_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['room_name']},
        ),
    ]