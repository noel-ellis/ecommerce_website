# Generated by Django 4.1.3 on 2023-02-19 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_deliveryinfo_zip"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deliveryinfo",
            name="zip",
            field=models.IntegerField(blank=True),
        ),
    ]
