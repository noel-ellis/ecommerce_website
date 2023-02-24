# Generated by Django 4.1.3 on 2023-02-19 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_remove_userbase_address_1_remove_userbase_address_2_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="deliveryinfo",
            name="name",
        ),
        migrations.RemoveField(
            model_name="deliveryinfo",
            name="phone_number",
        ),
        migrations.RemoveField(
            model_name="deliveryinfo",
            name="surname",
        ),
        migrations.AddField(
            model_name="userbase",
            name="name",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="userbase",
            name="phone_number",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="userbase",
            name="surname",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]