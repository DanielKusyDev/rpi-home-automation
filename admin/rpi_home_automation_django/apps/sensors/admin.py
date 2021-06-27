from apps.sensors.models import Sensor, SensorType
from django.contrib import admin

from apps.sensors.models import Device


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    readonly_fields = ["analog_output", "digital_output", "add_date"]
    list_display = ("device_specific_id", "device", "analog_output", "digital_output")


admin.site.register(SensorType)
admin.site.register(Device)
