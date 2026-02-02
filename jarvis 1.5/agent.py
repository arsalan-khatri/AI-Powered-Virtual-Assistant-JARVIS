import os
import sys
import datetime
import webbrowser
import pyautogui
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from weather import get_weather

# --- 🔇 SILENCER ---
try:
    null_device = "NUL" if os.name == "nt" else "/dev/null"
    f = open(null_device, 'w')
    os.dup2(f.fileno(), sys.stderr.fileno())
except:
    pass

# Gemini API config
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY not found in environment.")
    sys.exit()
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# TTS Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 190)

# --- FUNCTIONS ---
def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 1.0
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("\r(Listening...)", end="", flush=True)
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("\r" + " " * 30 + "\r", end="", flush=True)
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            print("\r" + " " * 30 + "\r", end="", flush=True)
            return None
        except Exception as e:
            print("Listen Error:", e)
            return None

def chat_with_gemini(prompt):
    try:
        system_instruction = "You are Jarvis. Answer in 1 short sentence (max 15 words)."
        full_prompt = f"{system_instruction}\nUser asks: {prompt}"
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=50,
                temperature=0.7
            )
        )
        return response.text.replace("*", "").replace("\n", " ")
    except Exception as e:
        print("Gemini Error:", e)
        return "I am having trouble connecting."

# --- SYSTEM COMMANDS ---
def execute_system_command(command):
    cmd = command.lower()

    # Websites
    if "open youtube" in cmd:
        speak("Opening YouTube, sir.")
        webbrowser.open("https://www.youtube.com")
        return True
    elif "open google" in cmd:
        speak("Opening Google, sir.")
        webbrowser.open("https://www.google.com")
        return True
    elif "open my website" in cmd:
        speak("Opening your website, sir.")
        webbrowser.open("https://akdeepknowledge.com")
        return True

    # Apps
    elif "open notepad" in cmd:
        speak("Opening Notepad.")
        os.system("start notepad")
        return True
    elif "open chrome" in cmd:
        speak("Opening Chrome.")
        os.system("start chrome")
        return True

    # Volume
    elif "volume up" in cmd:
        speak("Increasing volume.")
        pyautogui.press("volumeup", presses=5)
        return True
    elif "volume down" in cmd:
        speak("Decreasing volume.")
        pyautogui.press("volumedown", presses=5)
        return True
    elif "mute" in cmd:
        speak("Muting system.")
        pyautogui.press("volumemute")
        return True

    # Utility
    elif "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
        return True
    elif "hide all windows" in cmd:
        speak("Minimizing windows.")
        pyautogui.hotkey('win', 'd')
        return True

    # Weather
    elif "weather in" in cmd or "temperature in" in cmd:
        city = cmd.replace("weather in", "").replace("temperature in", "").strip()
        if not city:
            speak("Sir, which city should I check the weather for?")
            city = listen()
            if not city:
                speak("No city specified. Cancelling weather request.")
                return True

        weather_info = get_weather(city)
        speak(weather_info)
        return True

    return False

# --- MAIN LOOP ---
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------------------")
    print("   JARVIS AI ASSISTANT ONLINE   ")
    print("--------------------------------")

    speak("Hello sir, I am online and listening.")

    while True:
        user_command = listen()
        if user_command:
            print(f"You:    {user_command}")

            if "exit" in user_command.lower() or "stop" in user_command.lower() or "bye" in user_command.lower():
                speak("System shutting down. Goodbye.")
                sys.exit()

            if not execute_system_command(user_command):
                response = chat_with_gemini(user_command)
                speak(response)

            print("-" * 30)
