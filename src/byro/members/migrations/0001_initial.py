# Generated by Django 1.11.4 on 2017-08-12 10:46

import byro.common.models.auditable
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Member",
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
                ("email", models.EmailField(max_length=254)),
            ],
            bases=(byro.common.models.auditable.Auditable, models.Model),
        )
    ]
