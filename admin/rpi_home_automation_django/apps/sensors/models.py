from apps.plants.models import Plant
from django.db import models


class SensorTypeEnum(models.TextChoices):
    MOISTURE = "MOISTURE_SENSOR"
    TEMPERATURE = "TEMPERATURE_SENSOR"
    LIGHT_LEVEL = "LIGHT_LEVEL_SENSOR"


class Device(models.Model):
    name = models.CharField(max_length=64)
    mac_address = models.CharField(max_length=12, null=False)

    class Meta:
        verbose_name = "device"
        verbose_name_plural = "devices"

    def __str__(self) -> str:
        return self.name


class SensorType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "sensor type"
        verbose_name_plural = "sensor types"

    def __str__(self) -> str:
        return self.name


class Sensor(models.Model):
    device_specific_id = models.CharField(max_length=32, null=True, blank=True)
    plant = models.ForeignKey(to=Plant, on_delete=models.SET_NULL, null=True, blank=True)
    sensor_type = models.ForeignKey(to=SensorType, on_delete=models.SET_NULL, null=True, blank=True)
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    analog_output = models.FloatField(null=True, blank=True)
    digital_output = models.BooleanField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["device", "device_specific_id"], name="UQ_device__device_specific_id"),
        ]
        verbose_name = "sensor"
        verbose_name_plural = "sensors"

    def __str__(self) -> str:
        return f"{self.plant.name} [{self.sensor_type.name}]"
