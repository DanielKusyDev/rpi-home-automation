import json

from fastapi import HTTPException

from app.adapters.api_client import ForeignAPI
from app.domain.weather_entities import Weather

from app.config.settings import OPEN_WEATHER_API_KEY, LONGITUDE, LATITUDE, LANG


class OpenWeatherAPI(ForeignAPI):
    BASE_URL = "https://api.openweathermap.org/"


api = OpenWeatherAPI("data/2.5/weather")


def fetch() -> Weather:
    response = api.get(dict(lat=LATITUDE, lon=LONGITUDE, appid=OPEN_WEATHER_API_KEY, lang=LANG, units="metric"))
    response_data = json.loads(response.body.decode())
    if 200 <= response.status_code < 400:
        main_section = response_data["main"]
        summary_section = response_data["weather"][0]
        return Weather(
            description=summary_section["description"].capitalize(),
            icon=summary_section["icon"],
            temperature=main_section["temp"],
            pressure=main_section["pressure"],
            humidity=main_section["humidity"]
        )
    raise HTTPException(status_code=response.status_code, detail=response_data["message"])
