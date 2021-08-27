from apps.sensors.models import SensorTypeEnum

SENSOR_STATES_ICONS = {
    SensorTypeEnum.LIGHT_LEVEL.value: "fas fa-sun",
    SensorTypeEnum.MOISTURE.value: "fas fa-tint",
    SensorTypeEnum.TEMPERATURE.value: "fas fa-thermometer-full",
}
