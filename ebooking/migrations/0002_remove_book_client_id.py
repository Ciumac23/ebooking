# Generated by Django 4.0.1 on 2022-01-24 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebooking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='client_id',
        ),
    ]