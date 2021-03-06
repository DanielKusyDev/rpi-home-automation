# Generated by Django 3.2.2 on 2021-05-19 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sensors", "0005_add_analog_value_col_to_sensor_model"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sensor",
            name="analog_output",
        ),
        migrations.RemoveField(
            model_name="sensor",
            name="digital_output",
        ),
        migrations.AddField(
            model_name="sensor",
            name="analog_output",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="sensor",
            name="digital_output",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
