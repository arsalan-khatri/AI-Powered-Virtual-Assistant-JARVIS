from datetime import datetime
import requests
import os
import google.generativeai as genai

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY not found")
    exit()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

def get_weather(city):
    if not city:
        return "Sir, please specify the city."

    try:
        params = {"key": WEATHER_API_KEY, "q": city, "aqi": "no"}
        res = requests.get(BASE_URL, params=params, timeout=5).json()

        if "error" in res:
            return f"Weather API error: {res['error']['message']}"

        loc = res["location"]
        cur = res["current"]

        # Accurate temperature and day/night
        temp_c = round(cur["temp_c"])  # exact API value
        condition = cur["condition"]["text"]
        humidity = cur["humidity"]
        wind_kph = round(cur["wind_kph"])
        localtime = datetime.strptime(loc["localtime"], "%Y-%m-%d %H:%M")
        day_or_night = "day" if 6 <= localtime.hour < 18 else "night"

        # Friendly sentence (LLM does not modify values)
        prompt = (
            f"You are Jarvis, a friendly assistant.\n"
            f"City={loc['name']}, Temp={temp_c}°C, Condition={condition}, "
            f"Humidity={humidity}%, Wind={wind_kph} kph, It is {day_or_night}.\n"
            f"Task: Convert this into a short friendly sentence using the exact values."
            f"Do NOT add greetings like 'Hello' or 'Hi'. Only to-the-point weather info."
        )

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=50,
                temperature=0.7
            )
        )

        return response.text.replace("\n", " ")

    except Exception as e:
        return f"Could not fetch weather: {str(e)}"