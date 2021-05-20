from apps.plants.models import Plant
from django.db import models


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
    device_specific_id = models.CharField(max_length=32, null=True, blank=True)
    plant = models.ForeignKey(to=Plant, on_delete=models.SET_NULL, null=True, blank=True)
    sensor_type = models.ForeignKey(to=SensorType, on_delete=models.SET_NULL, null=True, blank=True)
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    analog_output = models.BooleanField(null=True, blank=True)
    digital_output = models.FloatField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["device", "device_specific_id"], name="UQ_device__device_specific_id"),
        ]

    def __str__(self) -> str:
        return f"{self.plant.name} [{self.sensor_type.name}]"


class Cli(models.Model):
    sensor = models.OneToOneField(to=Sensor, on_delete=models.SET_NULL, null=True, blank=True)
    module = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    parameters = models.CharField(max_length=511, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["module", "name", "parameters"], name="UQ_cli__module__name__parameters"),
        ]
