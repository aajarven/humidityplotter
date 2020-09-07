"""
Get the data from the OpenWeather API
"""

from datetime import datetime
import requests


def get_data(url, apikey):
    """
    Return data dict corresponding to the JSON from given url.
    """
    full_url = "{}&appid={}".format(url, apikey)
    response = requests.get(full_url)
    response.raise_for_status()
    return response.json()


def humidity_forecast(location, apikey):
    """
    Return a dict of humidity forecasts using timestamps as keys.
    """
    url = ("https://api.openweathermap.org/data/2.5/forecast?q={}"
           "".format(location))
    weathers = get_data(url, apikey)["list"]
    humidities = {}
    for weather in weathers:
        timestamp = datetime.strptime(weather["dt_txt"], "%Y-%m-%d %H:%M:%S")
        humidity = weather["main"]["humidity"]
        humidities[timestamp] = humidity
    return humidities
