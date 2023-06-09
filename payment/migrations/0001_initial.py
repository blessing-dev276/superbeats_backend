# Generated by Django 4.2 on 2023-04-03 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("drf_stripe", "0004_alter_productfeature_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                ("last4", models.CharField(max_length=10)),
                ("payment_id", models.CharField(max_length=255, unique=True)),
                (
                    "stripe_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="drf_stripe.stripeuser",
                    ),
                ),
            ],
        ),
    ]
