# Generated by Django 4.1.3 on 2023-01-23 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("store", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
