# Generated by Django 4.2.1 on 2023-05-15 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_remove_record_doctors_speciality_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='records',
        ),
    ]