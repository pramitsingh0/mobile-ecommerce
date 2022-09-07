# Generated by Django 4.1 on 2022-09-06 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mobile_store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="otp",
            field=models.CharField(max_length=6, null=True),
        ),
    ]
