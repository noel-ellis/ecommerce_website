# Generated by Django 4.1.3 on 2023-04-02 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="color",
        ),
        migrations.RemoveField(
            model_name="product",
            name="quantity",
        ),
        migrations.RemoveField(
            model_name="product",
            name="size",
        ),
        migrations.CreateModel(
            name="ProductVariant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("35", "35"),
                            ("36", "36"),
                            ("37", "37"),
                            ("38", "38"),
                            ("39", "39"),
                            ("40", "40"),
                            ("41", "41"),
                            ("42", "42"),
                            ("43", "43"),
                            ("44", "44"),
                            ("45", "45"),
                            ("46", "46"),
                            ("47", "47"),
                            ("48", "48"),
                            ("49", "49"),
                            ("50", "50"),
                        ],
                        max_length=4,
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                (
                    "color",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.color"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.product"
                    ),
                ),
            ],
        ),
    ]
