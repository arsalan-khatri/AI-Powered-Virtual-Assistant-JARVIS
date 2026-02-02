import os
import sys
import datetime
import webbrowser
import pyautogui
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from weather import get_weather
import shutil
import win32com.client
import asyncio
import wmi

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

def listen(timeout=7, phrase_time_limit=15):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 1.0
    recognizer.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("\r(Listening...)", end="", flush=True)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("\r" + " " * 30 + "\r", end="", flush=True)
            command = recognizer.recognize_google(audio)
            return command
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
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
    
    
    # --- FILE / FOLDER OPERATIONS ---
    elif "create folder" in cmd or "make folder" in cmd:
        try:
            # Step 1: Normalize command
            cleaned_cmd = cmd.lower()
            triggers = ["create folder", "make folder", "on desktop", "in desktop", "at desktop",
                        "on documents", "in documents", "at documents",
                        "on c drive", "in c drive", "at c drive",
                        "on d drive", "in d drive", "at d drive"]
            for word in triggers:
                cleaned_cmd = cleaned_cmd.replace(word, "")
            folder_name = cleaned_cmd.strip()  # remaining = possible folder name

            # Step 2: Determine base path
            base_path = None
            if "desktop" in cmd.lower():
                base_path = os.path.join(os.path.expanduser("~"), "Desktop")
            elif "documents" in cmd.lower():
                base_path = os.path.join(os.path.expanduser("~"), "Documents")
            elif "c drive" in cmd.lower():
                base_path = "C:\\"
            elif "d drive" in cmd.lower():
                base_path = "D:\\"
            else:
                # Ask user for location if not mentioned
                speak("Sir, where should I create the folder? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak("No location specified. Cancelling.")
                    return True
                location = location.strip().lower()
                if "desktop" in location:
                    base_path = os.path.join(os.path.expanduser("~"), "Desktop")
                elif "documents" in location:
                    base_path = os.path.join(os.path.expanduser("~"), "Documents")
                elif len(location) == 1 and location.isalpha():
                    base_path = f"{location.upper()}:\\"
                else:
                    base_path = location  # full path user ne diya

            # Step 3: Ask folder name if missing
            if not folder_name:
                speak("Sir, what should be the folder name?")
                folder_name = listen()
                if not folder_name:
                    speak("Sir, what should be the folder name again?")
                    folder_name = listen()

            # Step 4: Clean extra words in folder name
            folder_name = folder_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()

            # Step 5: Create folder
            full_path = os.path.join(base_path, folder_name)
            os.makedirs(full_path, exist_ok=True)
            speak(f"Folder {folder_name} created at {full_path}.")

        except Exception as e:
            speak(f"Could not create folder. Error: {str(e)}")
        return True

    # --- FILE CREATION (ADVANCED) ---
    elif "create file" in cmd:
        try:
            # Step 1: Normalize command
            cleaned_cmd = cmd.lower()
            triggers = ["create file", "on desktop", "in desktop", "at desktop",
                        "on documents", "in documents", "at documents",
                        "on c drive", "in c drive", "at c drive",
                        "on d drive", "in d drive", "at d drive"]
            for word in triggers:
                cleaned_cmd = cleaned_cmd.replace(word, "")
            file_name = cleaned_cmd.strip()  # remaining = possible file name

            # Step 2: Determine base path
            base_path = None
            if "desktop" in cmd.lower():
                base_path = os.path.join(os.path.expanduser("~"), "Desktop")
            elif "documents" in cmd.lower():
                base_path = os.path.join(os.path.expanduser("~"), "Documents")
            elif "c drive" in cmd.lower():
                base_path = "C:\\"
            elif "d drive" in cmd.lower():
                base_path = "D:\\"
            else:
                # Ask user for location if not mentioned
                speak("Sir, where should I create the file? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak("No location specified. Cancelling.")
                    return True
                location = location.strip().lower()
                if "desktop" in location:
                    base_path = os.path.join(os.path.expanduser("~"), "Desktop")
                elif "documents" in location:
                    base_path = os.path.join(os.path.expanduser("~"), "Documents")
                elif len(location) == 1 and location.isalpha():
                    base_path = f"{location.upper()}:\\"
                else:
                    base_path = location  # full path user ne diya

            # Step 3: Ask file name if missing
            if not file_name:
                speak("Sir, what should be the file name?")
                file_name = listen()
                if not file_name:
                    speak("No file name specified. Cancelling.")
                    return True

            # Step 4: Clean extra words in file name
            file_name = file_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()

            # Step 5: Ask for extension if missing
            name, ext = os.path.splitext(file_name)
            if not ext:
                max_attempts = 2
                for attempt in range(max_attempts):
                    speak("Sir, which extension should I use? For example, txt, py, or docx.")
                    user_ext = listen(timeout=10, phrase_time_limit=10)  # zyada time for user to speak
                    if user_ext:
                        user_ext = user_ext.strip().replace(".", "")
                        ext = "." + user_ext
                        break
                    else:
                        speak("I did not catch that.")
                else:
                    ext = ".txt"  # default if still no input
            file_name = name + ext


            # Step 6: Create file
            full_path = os.path.join(base_path, file_name)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)  # ensure folder exists
            with open(full_path, 'w') as f:
                f.write("")  # empty file

            speak(f"File {file_name} created at {full_path}.")

        except Exception as e:
            speak(f"Could not create file. Error: {str(e)}")
        return True



    # --- FILE DELETION (ADVANCED, EXTENSION ASK) ---
    elif "delete file" in cmd:
        try:
            # Step 1: Normalize command
            cleaned_cmd = cmd.lower()
            triggers = ["delete file", "on desktop", "in desktop", "at desktop",
                        "on documents", "in documents", "at documents",
                        "on c drive", "in c drive", "at c drive",
                        "on d drive", "in d drive", "at d drive"]
            for word in triggers:
                cleaned_cmd = cleaned_cmd.replace(word, "")
            file_name = cleaned_cmd.strip()  # remaining = possible file name

            # Step 2: Determine base path
            base_path = None
            cmd_lower = cmd.lower()
            if "desktop" in cmd_lower:
                base_path = os.path.join(os.path.expanduser("~"), "Desktop")
            elif "documents" in cmd_lower:
                base_path = os.path.join(os.path.expanduser("~"), "Documents")
            elif "c drive" in cmd_lower:
                if os.path.exists("C:\\"):
                    base_path = "C:\\"
                else:
                    speak("Sir, C drive does not exist.")
                    return True
            elif "d drive" in cmd_lower:
                if os.path.exists("D:\\"):
                    base_path = "D:\\"
                else:
                    speak("Sir, D drive does not exist.")
                    return True
            else:
                speak("Sir, where is the file located? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak("No location specified. Cancelling.")
                    return True
                location = location.strip()
                if location.lower() == "desktop":
                    base_path = os.path.join(os.path.expanduser("~"), "Desktop")
                elif location.lower() == "documents":
                    base_path = os.path.join(os.path.expanduser("~"), "Documents")
                elif len(location) == 1 and location.isalpha():
                    drive_path = f"{location.upper()}:\\"
                    if os.path.exists(drive_path):
                        base_path = drive_path
                    else:
                        speak(f"Sir, {location.upper()} drive does not exist.")
                        return True
                elif os.path.exists(location):
                    base_path = location  # full path user ne diya
                else:
                    speak(f"Sir, the specified path '{location}' does not exist.")
                    return True

            # Step 3: Ask file name if missing
            if not file_name:
                speak("Sir, what is the file name?")
                file_name = listen()
                if not file_name:
                    speak("No file name specified. Cancelling.")
                    return True

            # Step 4: Ask for extension if missing
            name, ext = os.path.splitext(file_name)
            if not ext:
                speak("Sir, which extension does the file have? For example, txt, py, or docx.")
                user_ext = listen(timeout=10, phrase_time_limit=10)
                if user_ext:
                    user_ext = user_ext.strip().replace(" dot ", ".").replace(" ", "")
                    if not user_ext.startswith("."):
                        user_ext = "." + user_ext
                    ext = user_ext
                else:
                    speak("No extension specified. Cancelling deletion.")
                    return True
            file_name = name + ext

            # Step 5: Clean extra words in file name
            file_name = file_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()

            # Step 6: Combine path and delete file
            full_path = os.path.join(base_path, file_name)
            if os.path.exists(full_path):
                os.remove(full_path)
                speak(f"File {file_name} deleted successfully from {full_path}.")
            else:
                speak(f"Sir, the file '{file_name}' does not exist at the specified location.")

        except Exception as e:
            speak(f"Could not delete file. Error: {str(e)}")
        return True

    # --- FILE OPEN (ADVANCED, EXTENSION ASK) ---
    elif "open file" in cmd:
        try:
            # Step 1: Normalize command
            cleaned_cmd = cmd.lower()
            triggers = ["open file", "on desktop", "in desktop", "at desktop",
                        "on documents", "in documents", "at documents",
                        "on c drive", "in c drive", "at c drive",
                        "on d drive", "in d drive", "at d drive"]
            for word in triggers:
                cleaned_cmd = cleaned_cmd.replace(word, "")
            file_name = cleaned_cmd.strip()  # remaining = possible file name
    
            # Step 2: Determine base path
            base_path = None
            cmd_lower = cmd.lower()
            if "desktop" in cmd_lower:
                base_path = os.path.join(os.path.expanduser("~"), "Desktop")
            elif "documents" in cmd_lower:
                base_path = os.path.join(os.path.expanduser("~"), "Documents")
            elif "c drive" in cmd_lower:
                if os.path.exists("C:\\"):
                    base_path = "C:\\"
                else:
                    speak("Sir, C drive does not exist.")
                    return True
            elif "d drive" in cmd_lower:
                if os.path.exists("D:\\"):
                    base_path = "D:\\"
                else:
                    speak("Sir, D drive does not exist.")
                    return True
            else:
                speak("Sir, where is the file located? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak("No location specified. Cancelling.")
                    return True
                location = location.strip()
                if location.lower() == "desktop":
                    base_path = os.path.join(os.path.expanduser("~"), "Desktop")
                elif location.lower() == "documents":
                    base_path = os.path.join(os.path.expanduser("~"), "Documents")
                elif len(location) == 1 and location.isalpha():
                    drive_path = f"{location.upper()}:\\"
                    if os.path.exists(drive_path):
                        base_path = drive_path
                    else:
                        speak(f"Sir, {location.upper()} drive does not exist.")
                        return True
                elif os.path.exists(location):
                    base_path = location  # full path user ne diya
                else:
                    speak(f"Sir, the specified path '{location}' does not exist.")
                    return True
    
            # Step 3: Ask file name if missing
            if not file_name:
                speak("Sir, what is the file name?")
                file_name = listen()
                if not file_name:
                    speak("No file name specified. Cancelling.")
                    return True
    
            # Step 4: Ask for extension if missing
            name, ext = os.path.splitext(file_name)
            if not ext:
                speak("Sir, which extension does the file have? For example, txt, py, or docx.")
                user_ext = listen(timeout=10, phrase_time_limit=10)
                if user_ext:
                    user_ext = user_ext.strip().replace(" dot ", ".").replace(" ", "")
                    if not user_ext.startswith("."):
                        user_ext = "." + user_ext
                    ext = user_ext
                else:
                    speak("No extension specified. Cancelling opening.")
                    return True
            file_name = name + ext
    
            # Step 5: Clean extra words in file name
            file_name = file_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()
    
            # Step 6: Combine path and open file
            full_path = os.path.join(base_path, file_name)
            if os.path.exists(full_path):
                os.startfile(full_path)
                speak(f"Opening file {file_name} from {full_path}.")
            else:
                speak(f"Sir, the file '{file_name}' does not exist at the specified location.")
    
        except Exception as e:
            speak(f"Could not open file. Error: {str(e)}")
        return True

    # --- FOLDER OPEN (ADVANCED) ---
    elif "open folder" in cmd:
        try:
            # Step 1: Normalize command
            cleaned_cmd = cmd.lower()
            triggers = ["open folder", "on desktop", "in desktop", "at desktop",
                        "on documents", "in documents", "at documents",
                        "on c drive", "in c drive", "at c drive",
                        "on d drive", "in d drive", "at d drive"]
            for word in triggers:
                cleaned_cmd = cleaned_cmd.replace(word, "")
            folder_name = cleaned_cmd.strip()  # remaining = possible folder name

            # Step 2: Determine base path
            base_path = None
            cmd_lower = cmd.lower()
            if "desktop" in cmd_lower:
                base_path = os.path.join(os.path.expanduser("~"), "Desktop")
            elif "documents" in cmd_lower:
                base_path = os.path.join(os.path.expanduser("~"), "Documents")
            elif "c drive" in cmd_lower:
                if os.path.exists("C:\\"):
                    base_path = "C:\\"
                else:
                    speak("Sir, C drive does not exist.")
                    return True
            elif "d drive" in cmd_lower:
                if os.path.exists("D:\\"):
                    base_path = "D:\\"
                else:
                    speak("Sir, D drive does not exist.")
                    return True
            else:
                # Ask user for location if not mentioned
                speak("Sir, where is the folder located? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak("No location specified. Cancelling.")
                    return True
                location = location.strip()
                if location.lower() == "desktop":
                    base_path = os.path.join(os.path.expanduser("~"), "Desktop")
                elif location.lower() == "documents":
                    base_path = os.path.join(os.path.expanduser("~"), "Documents")
                elif len(location) == 1 and location.isalpha():
                    drive_path = f"{location.upper()}:\\"
                    if os.path.exists(drive_path):
                        base_path = drive_path
                    else:
                        speak(f"Sir, {location.upper()} drive does not exist.")
                        return True
                elif os.path.exists(location):
                    base_path = location  # full path user ne diya
                else:
                    speak(f"Sir, the specified path '{location}' does not exist.")
                    return True

            # Step 3: Ask folder name if missing
            if not folder_name:
                speak("Sir, what is the folder name?")
                folder_name = listen()
                if not folder_name:
                    speak("No folder name specified. Cancelling.")
                    return True

            # Step 4: Clean extra words in folder name
            folder_name = folder_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()

            # Step 5: Combine path and open folder
            full_path = os.path.join(base_path, folder_name)
            if os.path.exists(full_path) and os.path.isdir(full_path):
                os.startfile(full_path)
                speak(f"Opening folder {folder_name} from {full_path}.")
            else:
                speak(f"Sir, the folder '{folder_name}' does not exist at the specified location.")

        except Exception as e:
            speak(f"Could not open folder. Error: {str(e)}")
        return True
    
    # --- FOLDER DELETION (SAME STYLE, NO CONFIRMATION) ---
    elif "delete folder" in cmd:
        try:
            # Step 1: Normalize command
            cleaned_cmd = cmd.lower()
            triggers = ["delete folder", "on desktop", "in desktop", "at desktop",
                        "on documents", "in documents", "at documents",
                        "on c drive", "in c drive", "at c drive",
                        "on d drive", "in d drive", "at d drive"]
            for word in triggers:
                cleaned_cmd = cleaned_cmd.replace(word, "")
            folder_name = cleaned_cmd.strip()  # remaining = possible folder name
    
            # Step 2: Determine base path
            base_path = None
            cmd_lower = cmd.lower()
    
            if "desktop" in cmd_lower:
                base_path = os.path.join(os.path.expanduser("~"), "Desktop")
            elif "documents" in cmd_lower:
                base_path = os.path.join(os.path.expanduser("~"), "Documents")
            elif "c drive" in cmd_lower:
                if os.path.exists("C:\\"):
                    base_path = "C:\\"
                else:
                    speak("Sir, C drive does not exist.")
                    return True
            elif "d drive" in cmd_lower:
                if os.path.exists("D:\\"):
                    base_path = "D:\\"
                else:
                    speak("Sir, D drive does not exist.")
                    return True
            else:
                speak("Sir, where is the folder located? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak("No location specified. Cancelling.")
                    return True
    
                location = location.strip().lower()
    
                if location == "desktop":
                    base_path = os.path.join(os.path.expanduser("~"), "Desktop")
                elif location == "documents":
                    base_path = os.path.join(os.path.expanduser("~"), "Documents")
                elif len(location) == 1 and location.isalpha():
                    drive_path = f"{location.upper()}:\\"
                    if os.path.exists(drive_path):
                        base_path = drive_path
                    else:
                        speak(f"Sir, {location.upper()} drive does not exist.")
                        return True
                elif os.path.exists(location):
                    base_path = location  # full path
                else:
                    speak(f"Sir, the specified path '{location}' does not exist.")
                    return True
    
            # Step 3: Ask folder name if missing
            if not folder_name:
                speak("Sir, what is the folder name?")
                folder_name = listen()
                if not folder_name:
                    speak("No folder name specified. Cancelling.")
                    return True
    
            # Step 4: Clean extra words
            folder_name = folder_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()
    
            # Step 5: Combine path
            full_path = os.path.join(base_path, folder_name)
    
            # Step 6: Delete folder
            if os.path.exists(full_path):
                shutil.rmtree(full_path)
                speak(f"Folder '{folder_name}' deleted successfully from {full_path}.")
            else:
                speak(f"Sir, the folder '{folder_name}' does not exist at the specified location.")
    
        except Exception as e:
            speak(f"Could not delete folder. Error: {str(e)}")
    
        return True
    
    elif "close folder" in cmd:
        import win32com.client
        try:
            # Step 1: Extract folder name from command
            folder_name = cmd.lower().replace("close folder", "").strip()

            # Step 2: Ask only if folder name missing
            if not folder_name:
                speak("Sir, which folder should I close?")
                folder_name = listen()
                if not folder_name:
                    speak("No folder name specified. Cancelling.")
                    return True
            else:
                speak(f"Closing folder '{folder_name}'...")

            folder_name = folder_name.lower()

            # Step 3: Close folder windows matching the name
            shell = win32com.client.Dispatch("Shell.Application")
            found = False
            for window in shell.Windows():
                try:
                    current_window_name = getattr(window, "LocationName", "").lower()
                    if folder_name in current_window_name:
                        window.Quit()
                        speak(f"Folder '{current_window_name}' closed successfully.")
                        found = True
                        break
                except:
                    continue

            if not found:
                speak(f"No open folder window found for '{folder_name}'.")

        except Exception as e:
            speak(f"Error closing folder: {e}")

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
