# Generated by Django 3.0 on 2022-08-06 05:48

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('back_end_application', '0001_initial'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='Supplier',
        #     fields=[
        #         ('supplierID', models.AutoField(primary_key=True, serialize=False)),
        #         ('name', models.CharField(max_length=100)),
        #         ('address', models.CharField(max_length=200)),
        #         ('phone', phone_field.models.PhoneField(max_length=31)),
        #     ],
        # ),
        # migrations.CreateModel(
        #     name='SupplyOrder',
        #     fields=[
        #         ('supplyOrderID', models.AutoField(primary_key=True, serialize=False)),
        #         ('invoiceNumber', models.CharField(default='000000000000', max_length=12)),
        #         ('date', models.DateTimeField()),
        #         ('supplierID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end_application.Supplier')),
        #     ],
        # ),
        # migrations.CreateModel(
        #     name='SupplyOrderStatus',
        #     fields=[
        #         ('updateID', models.AutoField(primary_key=True, serialize=False)),
        #         ('updateType', models.CharField(choices=[('DLY', 'Delayed'), ('DVD', 'Delivered'), ('SNT', 'Sent'), ('CNC', 'Cancelled'), ('OTH', 'Other')], max_length=512)),
        #         ('updateContents', models.CharField(max_length=512)),
        #         ('supplyOrderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end_application.SupplyOrder')),
        #     ],
        # ),
    ]
