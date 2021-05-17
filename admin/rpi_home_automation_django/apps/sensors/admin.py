from django.contrib import admin

from apps.sensors.models import Sensor, SensorType


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    readonly_fields = ["state", "add_date"]


admin.site.register(SensorType)
