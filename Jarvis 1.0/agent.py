import os
import sys
import time

# --- 🔇 SILENCER (Warnings Chupane ke liye) ---
try:
    null_device = "NUL" if os.name == "nt" else "/dev/null"
    f = open(null_device, 'w')
    os.dup2(f.fileno(), sys.stderr.fileno())
except:
    pass
# ----------------------------------------------

import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import datetime
import webbrowser
import pyautogui

# --- CONFIGURATION ---
API_KEY = "Enter Your API Key"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash') 

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 190) 

# --- FUNCTIONS ---

def speak(text):
    # Jarvis ka naam aur message print karein
    print(f"Jarvis: {text}") 
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    
    # --- 🔊 HIGH SENSITIVITY ---
    recognizer.energy_threshold = 300  
    recognizer.pause_threshold = 1.0   
    recognizer.dynamic_energy_threshold = True 
    
    with sr.Microphone() as source:
        # Temporary "Listening..." dikhayenge jo baad mein mit jayega
        print("\r(Listening...)", end="", flush=True)
        
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # "Listening" ko mita kar blank kar do
            print("\r" + " " * 30 + "\r", end="", flush=True)
            
            command = recognizer.recognize_google(audio)
            return command
            
        except sr.UnknownValueError:
            # Agar kuch samajh na aaye to line saaf kar do
            print("\r" + " " * 30 + "\r", end="", flush=True)
            return None
        except Exception:
            print("\r" + " " * 30 + "\r", end="", flush=True)
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
    except:
        return "I am having trouble connecting."
    
    
# --- 🛠️ SYSTEM CONTROL CENTER (Isse copy karein) ---
def execute_system_command(command):
    command = command.lower()

    # 1. Websites
    if "open youtube" in command:
        speak("Opening YouTube, sir.")
        webbrowser.open("https://www.youtube.com")
        return True
    elif "open google" in command:
        speak("Opening Google, sir.")
        webbrowser.open("https://www.google.com")
        return True
    elif "open ak deep knowledge" in command:
        speak("Opening your website, sir.")
        webbrowser.open("https://akdeepknowledge.com")
        return True

    # 2. System Apps
    elif "open notepad" in command:
        speak("Opening Notepad.")
        os.system("start notepad")
        return True
    elif "open chrome" in command:
        speak("Opening Chrome.")
        os.system("start chrome")
        return True

    # 3. Volume Control
    elif "volume up" in command:
        speak("Increasing volume.")
        pyautogui.press("volumeup", presses=5)
        return True
    elif "volume down" in command:
        speak("Decreasing volume.")
        pyautogui.press("volumedown", presses=5)
        return True
    elif "mute" in command:
        speak("Muting system.")
        pyautogui.press("volumemute")
        return True

    # 4. Utility
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        return True
    elif "minimize" in command:
        speak("Minimizing windows.")
        pyautogui.hotkey('win', 'd')
        return True

    return False # Agar command system ki nahi thi

# --- MAIN LOOP ---

if __name__ == "__main__":
    # Screen Clear
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Header Design
    print("--------------------------------")
    print("   JARVIS AI ASSISTANT ONLINE   ")
    print("--------------------------------")
    
    # 1. Sabse pehle Jarvis bolega (Startup)
    speak("Hello sir, I am online and listening.")
    
    # while True:
    #     user_command = listen()
        
    #     if user_command:
    #         # 2. User ka message print karein "You: ..." style mein
    #         print(f"You:    {user_command}")
            
    #         # Exit Logic
    #         if "exit" in user_command.lower() or "stop" in user_command.lower():
    #             speak("System shutting down. Goodbye.")
    #             sys.exit()
            
    #         # 3. Jarvis ka response
    #         response = chat_with_gemini(user_command)
    #         speak(response)
            
    #         # Thora gap taake saaf dikhe
    #         print("-" * 30)
    while True:
        user_command = listen()
        
        if user_command:
            print(f"You:    {user_command}")
            
            # Exit Check
            if "exit" in user_command.lower() or "stop" in user_command.lower():
                speak("System shutting down. Goodbye.")
                sys.exit()

            # --- YE LINE ZAROORI HAI (System check) ---
            if not execute_system_command(user_command):
                # Agar system command nahi thi, tabhi Gemini se poocho
                response = chat_with_gemini(user_command)
                speak(response)
            
            print("-" * 30)