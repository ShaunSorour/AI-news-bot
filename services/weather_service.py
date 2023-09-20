import requests
from secret import weather_base_url, icon_url
from dotenv import load_dotenv
load_dotenv()
import os


def get_weather(city):
    try:
        API_KEY = os.getenv("API_KEY")
        url = f"{weather_base_url}{city}&appid={API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print("Error getting weather data:", e)


def weather_details(city):
    weather_data = get_weather(city)
    if weather_data:
        temperature_kelvin = weather_data["main"]["temp"]
        temp_full = temperature_kelvin - 273.15
        temp = round(temp_full)
        description = weather_data["weather"][0]["description"]
        weather_icon = weather_data["weather"][0]["icon"]
        iconURL = f"{icon_url}{weather_icon}@2x.png"
        print("Weather successfully retrieved")

        weather = {
            "temp": temp,
            "description": description,
            "iconURL": iconURL
        }

        return weather
    else:
        return "No Weather Data Found"