# Generated by Django 3.2.4 on 2021-12-31 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0002_alter_ticketreport_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='revision',
            name='state',
            field=models.CharField(choices=[('R', 'Revisado'), ('P', 'Pendiente')], default='P', max_length=1),
        ),
    ]