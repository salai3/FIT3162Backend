# Generated by Django 3.0 on 2022-09-19 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back_end_application', '0004_auto_20220920_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='productID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end_application.Product'),
        ),
    ]
