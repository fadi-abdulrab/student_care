# Generated by Django 3.1 on 2022-07-04 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0007_auto_20220704_0805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='session_year_id',
        ),
        migrations.DeleteModel(
            name='SessionYearModel',
        ),
    ]