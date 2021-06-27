from apps.plants.models import Plant
from config.resources import SENSOR_STATES_ICONS
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.sensors.models import Sensor, SensorTypeEnum


class PlantAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css",)}

    list_display = ("name", "description", "sensors", "image")

    def sensors(self, obj: Plant) -> str:
        def sensor_to_icon(sensor: Sensor):
            if sensor.sensor_type.name == SensorTypeEnum.MOISTURE.value:
                color = "green" if sensor.digital_output else "red"
            else:
                color = "orange"
            return f"""
            <a href="{reverse("admin:sensors_sensor_change", kwargs={"object_id": sensor.pk})}">
                <i style="color: {color}" class="{SENSOR_STATES_ICONS[sensor.sensor_type.name]} fa-2x"></i>
            </a>    
            """

        return mark_safe("".join(sensor_to_icon(sensor) for sensor in obj.sensor_set.all()))

    sensors.short_description = "Sensors"


admin.site.register(Plant, PlantAdmin)
