# Generated by Django 4.1.3 on 2023-04-03 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_rename_quantity_productvariant_available_units"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ("-date_modified",),
                "verbose_name_plural": "Products",
            },
        ),
        migrations.AlterModelOptions(
            name="productvariant",
            options={"verbose_name_plural": "Product Variants"},
        ),
        migrations.RemoveField(
            model_name="product",
            name="image",
        ),
        migrations.AddField(
            model_name="productvariant",
            name="image",
            field=models.ImageField(
                blank=True, default="default_item.png", upload_to="product_pics"
            ),
        ),
    ]
