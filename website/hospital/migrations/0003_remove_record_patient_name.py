# Generated by Django 4.2.1 on 2023-05-14 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_alter_customuser_records'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='patient_name',
        ),
    ]