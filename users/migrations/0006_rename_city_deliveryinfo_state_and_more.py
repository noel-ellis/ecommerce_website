# Generated by Django 4.1.3 on 2023-02-19 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_remove_deliveryinfo_name_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="deliveryinfo",
            old_name="city",
            new_name="state",
        ),
        migrations.RenameField(
            model_name="deliveryinfo",
            old_name="postcode",
            new_name="zip",
        ),
    ]