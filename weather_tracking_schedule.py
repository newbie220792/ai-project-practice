import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
import paho.mqtt.client as mqtt
import json


def load_wmo_codes():
    return json.load(open("wmo_code.json", "r"))

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# setup broker client for MQTT
broker = "localhost"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker, 1883, 60)

def weather_tracking_schedule():
    # def weather_tracking_schedule():
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 10.958029338330077,
        "longitude": 106.79836897304934,
        "current": ["temperature_2m", "relative_humidity_2m", "rain", "weather_code", "cloud_cover", "wind_speed_10m", "apparent_temperature", "is_day"],
        "timezone": "GMT",
        "forecast_days": 1,
    }
    responses = openmeteo.weather_api(url, params = params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation: {response.Elevation()} m asl")
    # print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process current data. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_rain = current.Variables(2).Value()
    current_weather_code = int(current.Variables(3).Value())

    current_cloud_cover = current.Variables(4).Value()
    current_wind_speed_10m = current.Variables(5).Value()
    current_apparent_temperature = current.Variables(6).Value()
    current_is_day = int(current.Variables(7).Value())

    weather_code_mapping = load_wmo_codes()
    # print(f"Current weather_code: {current_weather_code}")
    current_weather = weather_code_mapping.get(str(current_weather_code), "Unknown")
    # print(f"Current weather: {current_weather}")
    if current_is_day == 1 :
        current_weather_time =  current_weather["day"] 
    else: 
        current_weather_time = current_weather["night"]

    client.publish("weather/temperature", current_temperature_2m)
    client.publish("weather/humidity", current_relative_humidity_2m)
    client.publish("weather/rain", current_rain)
    client.publish("weather/cloud_cover", current_cloud_cover)
    client.publish("weather/wind_speed_10m", current_wind_speed_10m)
    client.publish("weather/apparent_temperature", current_apparent_temperature)
    client.publish("weather/is_day", current_is_day)
    client.publish("weather/weather_description", current_weather_time['description'])

    client.subscribe("weather/#")

    # print(f"\nCurrent time: {current.Time()}")
    # print(f"Current temperature_2m: {current_temperature_2m}")
    # print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")
    # print(f"Current rain: {current_rain}")

    # print(f"Current cloud_cover: {current_cloud_cover}")
    # print(f"Current wind_speed_10m: {current_wind_speed_10m}")
    # print(f"Current apparent_temperature: {current_apparent_temperature}")
    # print(f"Current is_day: { True if current_is_day == 1 else False }")
    # print(f"Current weather_description: {current_weather_time['description']}")

weather_tracking_schedule()