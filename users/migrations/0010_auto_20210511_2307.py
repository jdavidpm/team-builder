# Generated by Django 3.1.7 on 2021-05-12 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210501_1241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='income_semester',
            new_name='entry_semester',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='income_year',
            new_name='entry_year',
        ),
    ]