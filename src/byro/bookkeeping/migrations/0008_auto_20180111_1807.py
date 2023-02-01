# Generated by Django 1.11.8 on 2018-01-11 18:07

import byro.common.models.auditable
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("bookkeeping", "0007_auto_20171206_1919")]

    operations = [
        migrations.CreateModel(
            name="RealTransactionSource",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("source_file", models.FileField(upload_to="transaction_uploads/")),
            ],
            bases=(byro.common.models.auditable.Auditable, models.Model),
        ),
        migrations.AddField(
            model_name="realtransaction",
            name="source",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="transactions",
                to="bookkeeping.RealTransactionSource",
            ),
        ),
    ]
