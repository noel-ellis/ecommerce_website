# Generated by Django 4.1.3 on 2022-12-08 12:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("quantity", models.PositiveIntegerField()),
                ("price", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True, default="default_item.png", upload_to="product_pics"
                    ),
                ),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.category"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Products",
                "ordering": ("-date_modified",),
            },
        ),
        migrations.CreateModel(
            name="Cart",
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
                ("quantity", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("IC", "waiting for confirmation"),
                            ("AC", "accepted"),
                            ("PR", "processing"),
                            ("SE", "sent"),
                            ("RE", "waiting for delivery"),
                            ("DE", "successfully delivered"),
                        ],
                        default="IC",
                        max_length=2,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.product"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
