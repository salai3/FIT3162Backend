# Generated by Django 3.0 on 2022-09-11 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back_end_application', '0003_auto_20220911_1649'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='User',
            new_name='user',
        ),
    ]
