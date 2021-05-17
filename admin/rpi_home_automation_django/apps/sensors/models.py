from django.db import models

from apps.plants.models import Plant


class DeviceEnum(models.TextChoices):
    RASPBERRY_PI = "RPI"


class SensorTypeEnum(models.TextChoices):
    MOISTURE = "MOISTURE"
    TEMPERATURE = "TEMPERATURE"
    LIGHT = "LIGHT"


class Device(models.Model):
    name = models.CharField(max_length=15, choices=DeviceEnum.choices)
    mac_address = models.CharField(max_length=12, null=False)

    def __str__(self) -> str:
        return self.name


class SensorType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Sensor(models.Model):
    plant = models.ForeignKey(to=Plant, on_delete=models.SET_NULL, null=True, blank=True)
    sensor_type = models.ForeignKey(to=SensorType, on_delete=models.SET_NULL, null=True, blank=True)
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.plant.name} [{self.sensor_type.name}]"
