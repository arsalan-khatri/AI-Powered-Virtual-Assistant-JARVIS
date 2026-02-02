import requests
from datetime import datetime
import os

# --- CONFIG ---
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Apni WeatherAPI key
CITY = "Karachi"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def test_weather(city):
    try:
        params = {"key": WEATHER_API_KEY, "q": city, "aqi": "no"}
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if "error" in data:
            print("Weather API error:", data["error"]["message"])
            return

        loc = data["location"]
        cur = data["current"]

        # --- Temperature Calculation ---
        temp_c = cur["temp_c"]
        temp_f = round((temp_c * 9/5) + 32, 1)

        # --- Day/Night Logic ---
        localtime_str = loc["localtime"]  # Format: YYYY-MM-DD HH:MM
        localtime = datetime.strptime(localtime_str, "%Y-%m-%d %H:%M")
        hour = localtime.hour
        day_or_night = "day" if 6 <= hour < 18 else "night"

        # --- Other Info ---
        condition = cur["condition"]["text"]
        humidity = cur["humidity"]
        wind_kph = round(cur["wind_kph"])

        # --- Print Results ---
        print(f"Weather for {loc['name']}, {loc['country']}:")
        print(f"Temperature: {temp_c}°C / {temp_f}°F")
        print(f"Condition: {condition}")
        print(f"Humidity: {humidity}%")
        print(f"Wind: {wind_kph} kph")
        print(f"It is currently {day_or_night}.")
        print(f"Local time: {localtime_str}")

    except Exception as e:
        print("Error fetching weather:", str(e))

# --- Run Test ---
test_weather(CITY)
