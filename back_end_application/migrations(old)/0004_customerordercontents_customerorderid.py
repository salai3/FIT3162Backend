# Generated by Django 3.0 on 2022-09-10 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back_end_application', '0003_batch_batchstatus_customer_customerorder_customerordercontents'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerordercontents',
            name='customerOrderID',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='back_end_application.CustomerOrder'),
            preserve_default=False,
        ),
    ]