from apps.sensors.models import Sensor, SensorType
from django.contrib import admin


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    readonly_fields = ["analog_output", "digital_output", "add_date"]
    list_display = ("device_specific_id", "analog_output", "digital_output")


admin.site.register(SensorType)
