from apps.sensors.models import Sensor, SensorType
from django.contrib import admin


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    readonly_fields = ["analog_output", "digital_output", "add_date"]


admin.site.register(SensorType)
