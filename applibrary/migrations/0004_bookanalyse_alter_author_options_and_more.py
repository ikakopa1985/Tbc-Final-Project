# Generated by Django 4.2.13 on 2024-05-17 12:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "applibrary",
            "0003_cancelreserve_lease_receive_reserve_alter_book_stock_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="BookAnalyse",
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
            ],
        ),
        migrations.AlterModelOptions(
            name="author",
            options={},
        ),
        migrations.AlterField(
            model_name="lease",
            name="must_receive_date",
            field=models.DateField(null=True, verbose_name="must_receive_date"),
        ),
    ]
