# Generated by Django 3.0 on 2022-09-20 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_end_application', '0006_customerordercontents_supplierid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerorder',
            old_name='date',
            new_name='dateCreated',
        ),
        migrations.AddField(
            model_name='customerorder',
            name='lastUpdated',
            field=models.DateTimeField(default='2022-09-20 09:51:38.570162+01:00'),
            preserve_default=False,
        ),
    ]
