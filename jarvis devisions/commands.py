import os
import shutil
import webbrowser
import pyautogui
from utils import speak_urdu, listen
# generate_image_tool
from weather import get_weather
import datetime
import subprocess
import pywhatkit
# --- SYSTEM COMMANDS ---
def execute_system_command(command):
    cmd = command.lower()
    # --- Websites (Smart Close: Sirf Tab band karega) ---
    if "youtube" in cmd and ("open" in cmd or "chalao" in cmd):
        speak_urdu("Opening YouTube, sir.")
        webbrowser.open("https://www.youtube.com")
        return True

    elif "close youtube" in cmd:
        speak_urdu("Closing YouTube tab, sir.")
        # Ye CTRL + W dabayega, jo sirf active tab close karta hai
        pyautogui.hotkey('ctrl', 'w') 
        return True

    elif "open google" in cmd:
        speak_urdu("Opening Google, sir.")
        webbrowser.open("https://www.google.com")
        return True

    elif "close google" in cmd:
        speak_urdu("Closing Google tab, sir.")
        pyautogui.hotkey('ctrl', 'w')
        return True

    elif "open my website" in cmd:
        speak_urdu("Opening AK Deep Knowledge, sir.")
        webbrowser.open("https://akdeepknowledge.com")
        return True

    elif "close my website" in cmd:
        speak_urdu("Closing your website tab, sir.")
        pyautogui.hotkey('ctrl', 'w')
        return True

    # --- Apps (Smart Close: Sirf Window band karega) ---
    elif "open notepad" in cmd:
        speak_urdu("Opening Notepad.")
        os.system("start notepad")
        return True

    elif "close notepad" in cmd:
        speak_urdu("Closing Notepad.")
        # Notepad ke liye Taskkill theek hai, lekin Alt+F4 zyada safe hai
        # Taki wo save karne ka option de agar kuch likha ho
        pyautogui.hotkey('alt', 'f4') 
        return True

    elif "open chrome" in cmd or "open browser" in cmd:
        # Check karein ke Chrome pehle se chal raha hai ya nahi
        try:
            # Tasklist se running processes ki list nikal rahe hain
            process_list = subprocess.check_output('tasklist', shell=True).decode().lower()
        except Exception as e:
            process_list = ""

        if "chrome.exe" in process_list:
            # Agar Chrome already open hai
            speak_urdu("Sir, Chrome is already open. Kya aap new window open karna chahte hain?")
            
            # --- YAHAN DHYAN DEIN ---
            # Yahan aapko apna mic sunne wala function call karna hai. 
            # Maan lijiye wo 'take_command()' hai.
            confirmation = listen().lower() 
            
            if "yes" in confirmation or "ha" in confirmation or "ji" in confirmation or "open" in confirmation:
                speak_urdu("Okay sir, opening a new Chrome window.")
                # '/new-window' flag use kar rahe hain taaki fresh window khule
                os.system("start chrome /new-window")
            else:
                speak_urdu("Okay sir, leaving it as is.")
        
        else:
            # Agar Chrome band hai, to normal open karein (Default Profile)
            speak_urdu("Opening Chrome browser.")
            os.system("start chrome")
            
    elif "close chrome" in cmd or "close browser" in cmd:
        # Step 1: Check karein ke Chrome chal bhi raha hai ya nahi
        try:
            process_list = subprocess.check_output('tasklist', shell=True).decode().lower()
        except Exception:
            process_list = ""

        if "chrome.exe" in process_list:
            # Step 2: User se puchen ke kis level ka close karna hai
            speak_urdu("Sir, Chrome is running. Kya main sirf Current Window close karun ya Sab kuch (All) band kar dun?")
            
            # Yahan apna mic function call karein (e.g., take_command())
            mode = listen().lower() 

            if "all" in mode or "sab" in mode or "everything" in mode:
                # OPTION A: Disaster Mode (Sirf tab jab user bole 'Sab band karo')
                speak_urdu("Okay sir, closing all Chrome instances.")
                os.system("taskkill /IM chrome.exe /F")
            
            elif "current" in mode or "active" in mode or "ye wali" in mode or "one" in mode:
                # OPTION B: Safe Mode (Sirf samne wali window)
                speak_urdu("Okay, closing current window.")
                pyautogui.hotkey('alt', 'f4')
            
            else:
                # Agar user kuch aur bole ya samajh na aaye, to Safe Mode use karein
                speak_urdu("Okay, closing the active window safely.")
                pyautogui.hotkey('alt', 'f4')

        else:
            speak_urdu("Sir, Chrome pehle se hi band hai.")
            return True
        
    #     # --- YouTube Play Command ---
    elif "play" in cmd or "youtube" in cmd:
        # 1. Badi list banayein taake har tarah ka kachra saaf ho sake
        stopwords = [
            "play", "youtube", "on", "pe", "chalao", "chala", "laga", "do", "karo", 
            "please", "jarvis", "sunao", "suna", "ka", "ki", "ke", "wala", "wali", 
            "bhai", "yaar", "are", "meri", "mere", "liye", "jo", "hai", "wo", "vah"
        ]
        
        # 2. Command se stopwords remove karein
        query = cmd
        for word in stopwords:
            # Hum words ko replace karte waqt spaces ka khayal rakhenge
            # Taake "play" replace ho, lekin "player" kharab na ho
            query = query.replace(f" {word} ", " ") # Beech ke words
            query = query.replace(f"{word} ", " ")  # Shuru ke words
            query = query.replace(f" {word}", " ")  # Aakhir ke words

        # 3. Final cleaning (extra spaces hatana)
        song_name = " ".join(query.split())

        print(f"DEBUG: Original -> '{cmd}'")
        print(f"DEBUG: Extracted -> '{song_name}'")

        if song_name:
            speak_urdu(f"Playing {song_name} on YouTube.")
            try:
                # pywhatkit kabhi kabhi time leta hai, isliye try-except lagaya
                pywhatkit.playonyt(song_name)
            except Exception as e:
                speak_urdu("Sir, network issue ki wajah se play nahi ho raha.")
                print(e)
        else:
            speak_urdu("Sir, aapne song ka naam nahi bataya.")
            
        return True
    
    # --- Image Generation Command ---
    # elif "generate image" in command or "create image" in command or "make an image" in command:
    #     speak_urdu("Sure, what should I draw?")
        
    #     # User se prompt lene ke liye dubara sunna padega
    #     # Agar aapke paas 'take_command()' function hai to usay call karein
    #     # Ya phir isi command me se text nikaal lein agar user ne ek sath bola ho
        
    #     # Example 1: User ne bola "Generate image of a flying car"
    #     prompt = command.replace("generate image", "").replace("create image", "").replace("make an image", "").replace("of", "", 1).strip()
        
    #     # Agar command me prompt nahi tha, to dubara poochein
    #     if not prompt:
    #         prompt = listen() # Ye aapka mic wala function hona chahiye
        
    #     if prompt:
    #         speak_urdu(f"Generating an image of {prompt}, please wait...")
    #         success = generate_image_tool(prompt)
            
    #         if success:
    #             speak_urdu("Image generated successfully, Sir.")
    #         else:
    #             speak_urdu("Sorry, I faced an error while generating the image.")
    #     else:
    #         speak_urdu("I didn't hear the prompt properly.")

    # Volume
    elif "volume up" in cmd:
        speak_urdu("Increasing volume.")
        pyautogui.press("volumeup", presses=5)
        return True
    elif "volume down" in cmd:
        speak_urdu("Decreasing volume.")
        pyautogui.press("volumedown", presses=5)
        return True
    elif "mute" in cmd:
        speak_urdu("Muting system.")
        pyautogui.press("volumemute")
        return True

    # Utility
    elif "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak_urdu(f"The current time is {now}")
        return True
    elif "hide all windows" in cmd:
        speak_urdu("Minimizing windows.")
        pyautogui.hotkey('win', 'd')
        return True

    # Weather
    elif "weather in" in cmd or "temperature in" in cmd:
        city = cmd.replace("weather in", "").replace("temperature in", "").strip()
        if not city:
            speak_urdu("Sir, which city should I check the weather for?")
            city = listen()
            if not city:
                speak_urdu("No city specified. Cancelling weather request.")
                return True

        weather_info = get_weather(city)
        speak_urdu(weather_info)
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
                speak_urdu("Sir, where should I create the folder? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak_urdu("No location specified. Cancelling.")
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
                speak_urdu("Sir, what should be the folder name?")
                folder_name = listen()
                if not folder_name:
                    speak_urdu("Sir, what should be the folder name again?")
                    folder_name = listen()

            # Step 4: Clean extra words in folder name
            folder_name = folder_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()

            # Step 5: Create folder
            full_path = os.path.join(base_path, folder_name)
            os.makedirs(full_path, exist_ok=True)
            speak_urdu(f"Folder {folder_name} created at {full_path}.")

        except Exception as e:
            speak_urdu(f"Could not create folder. Error: {str(e)}")
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
                speak_urdu("Sir, where should I create the file? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak_urdu("No location specified. Cancelling.")
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
                speak_urdu("Sir, what should be the file name?")
                file_name = listen()
                if not file_name:
                    speak_urdu("No file name specified. Cancelling.")
                    return True

            # Step 4: Clean extra words in file name
            file_name = file_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()

            # Step 5: Ask for extension if missing
            name, ext = os.path.splitext(file_name)
            if not ext:
                max_attempts = 2
                for attempt in range(max_attempts):
                    speak_urdu("Sir, which extension should I use? For example, txt, py, or docx.")
                    user_ext = listen(timeout=10, phrase_time_limit=10)  # zyada time for user to speak_urdu
                    if user_ext:
                        user_ext = user_ext.strip().replace(".", "")
                        ext = "." + user_ext
                        break
                    else:
                        speak_urdu("I did not catch that.")
                else:
                    ext = ".txt"  # default if still no input
            file_name = name + ext


            # Step 6: Create file
            full_path = os.path.join(base_path, file_name)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)  # ensure folder exists
            with open(full_path, 'w') as f:
                f.write("")  # empty file

            speak_urdu(f"File {file_name} created at {full_path}.")

        except Exception as e:
            speak_urdu(f"Could not create file. Error: {str(e)}")
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
                    speak_urdu("Sir, C drive does not exist.")
                    return True
            elif "d drive" in cmd_lower:
                if os.path.exists("D:\\"):
                    base_path = "D:\\"
                else:
                    speak_urdu("Sir, D drive does not exist.")
                    return True
            else:
                speak_urdu("Sir, where is the file located? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak_urdu("No location specified. Cancelling.")
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
                        speak_urdu(f"Sir, {location.upper()} drive does not exist.")
                        return True
                elif os.path.exists(location):
                    base_path = location  # full path user ne diya
                else:
                    speak_urdu(f"Sir, the specified path '{location}' does not exist.")
                    return True

            # Step 3: Ask file name if missing
            if not file_name:
                speak_urdu("Sir, what is the file name?")
                file_name = listen()
                if not file_name:
                    speak_urdu("No file name specified. Cancelling.")
                    return True

            # Step 4: Ask for extension if missing
            name, ext = os.path.splitext(file_name)
            if not ext:
                speak_urdu("Sir, which extension does the file have? For example, txt, py, or docx.")
                user_ext = listen(timeout=10, phrase_time_limit=10)
                if user_ext:
                    user_ext = user_ext.strip().replace(" dot ", ".").replace(" ", "")
                    if not user_ext.startswith("."):
                        user_ext = "." + user_ext
                    ext = user_ext
                else:
                    speak_urdu("No extension specified. Cancelling deletion.")
                    return True
            file_name = name + ext

            # Step 5: Clean extra words in file name
            file_name = file_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()

            # Step 6: Combine path and delete file
            full_path = os.path.join(base_path, file_name)
            if os.path.exists(full_path):
                os.remove(full_path)
                speak_urdu(f"File {file_name} deleted successfully from {full_path}.")
            else:
                speak_urdu(f"Sir, the file '{file_name}' does not exist at the specified location.")

        except Exception as e:
            speak_urdu(f"Could not delete file. Error: {str(e)}")
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
                    speak_urdu("Sir, C drive does not exist.")
                    return True
            elif "d drive" in cmd_lower:
                if os.path.exists("D:\\"):
                    base_path = "D:\\"
                else:
                    speak_urdu("Sir, D drive does not exist.")
                    return True
            else:
                speak_urdu("Sir, where is the file located? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak_urdu("No location specified. Cancelling.")
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
                        speak_urdu(f"Sir, {location.upper()} drive does not exist.")
                        return True
                elif os.path.exists(location):
                    base_path = location  # full path user ne diya
                else:
                    speak_urdu(f"Sir, the specified path '{location}' does not exist.")
                    return True
    
            # Step 3: Ask file name if missing
            if not file_name:
                speak_urdu("Sir, what is the file name?")
                file_name = listen()
                if not file_name:
                    speak_urdu("No file name specified. Cancelling.")
                    return True
    
            # Step 4: Ask for extension if missing
            name, ext = os.path.splitext(file_name)
            if not ext:
                speak_urdu("Sir, which extension does the file have? For example, txt, py, or docx.")
                user_ext = listen(timeout=10, phrase_time_limit=10)
                if user_ext:
                    user_ext = user_ext.strip().replace(" dot ", ".").replace(" ", "")
                    if not user_ext.startswith("."):
                        user_ext = "." + user_ext
                    ext = user_ext
                else:
                    speak_urdu("No extension specified. Cancelling opening.")
                    return True
            file_name = name + ext
    
            # Step 5: Clean extra words in file name
            file_name = file_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()
    
            # Step 6: Combine path and open file
            full_path = os.path.join(base_path, file_name)
            if os.path.exists(full_path):
                os.startfile(full_path)
                speak_urdu(f"Opening file {file_name} from {full_path}.")
            else:
                speak_urdu(f"Sir, the file '{file_name}' does not exist at the specified location.")
    
        except Exception as e:
            speak_urdu(f"Could not open file. Error: {str(e)}")
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
                    speak_urdu("Sir, C drive does not exist.")
                    return True
            elif "d drive" in cmd_lower:
                if os.path.exists("D:\\"):
                    base_path = "D:\\"
                else:
                    speak_urdu("Sir, D drive does not exist.")
                    return True
            else:
                # Ask user for location if not mentioned
                speak_urdu("Sir, where is the folder located? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak_urdu("No location specified. Cancelling.")
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
                        speak_urdu(f"Sir, {location.upper()} drive does not exist.")
                        return True
                elif os.path.exists(location):
                    base_path = location  # full path user ne diya
                else:
                    speak_urdu(f"Sir, the specified path '{location}' does not exist.")
                    return True

            # Step 3: Ask folder name if missing
            if not folder_name:
                speak_urdu("Sir, what is the folder name?")
                folder_name = listen()
                if not folder_name:
                    speak_urdu("No folder name specified. Cancelling.")
                    return True

            # Step 4: Clean extra words in folder name
            folder_name = folder_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()

            # Step 5: Combine path and open folder
            full_path = os.path.join(base_path, folder_name)
            if os.path.exists(full_path) and os.path.isdir(full_path):
                os.startfile(full_path)
                speak_urdu(f"Opening folder {folder_name} from {full_path}.")
            else:
                speak_urdu(f"Sir, the folder '{folder_name}' does not exist at the specified location.")

        except Exception as e:
            speak_urdu(f"Could not open folder. Error: {str(e)}")
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
                    speak_urdu("Sir, C drive does not exist.")
                    return True
            elif "d drive" in cmd_lower:
                if os.path.exists("D:\\"):
                    base_path = "D:\\"
                else:
                    speak_urdu("Sir, D drive does not exist.")
                    return True
            else:
                speak_urdu("Sir, where is the folder located? You can say Desktop, Documents, a drive, or full path.")
                location = listen()
                if not location:
                    speak_urdu("No location specified. Cancelling.")
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
                        speak_urdu(f"Sir, {location.upper()} drive does not exist.")
                        return True
                elif os.path.exists(location):
                    base_path = location  # full path
                else:
                    speak_urdu(f"Sir, the specified path '{location}' does not exist.")
                    return True
    
            # Step 3: Ask folder name if missing
            if not folder_name:
                speak_urdu("Sir, what is the folder name?")
                folder_name = listen()
                if not folder_name:
                    speak_urdu("No folder name specified. Cancelling.")
                    return True
    
            # Step 4: Clean extra words
            folder_name = folder_name.replace(" on", "").replace(" at", "").replace(" in", "").strip()
    
            # Step 5: Combine path
            full_path = os.path.join(base_path, folder_name)
    
            # Step 6: Delete folder
            if os.path.exists(full_path):
                shutil.rmtree(full_path)
                speak_urdu(f"Folder '{folder_name}' deleted successfully from {full_path}.")
            else:
                speak_urdu(f"Sir, the folder '{folder_name}' does not exist at the specified location.")
    
        except Exception as e:
            speak_urdu(f"Could not delete folder. Error: {str(e)}")
    
        return True
    
    elif "close folder" in cmd:
        import win32com.client
        try:
            # Step 1: Extract folder name from command
            folder_name = cmd.lower().replace("close folder", "").strip()

            # Step 2: Ask only if folder name missing
            if not folder_name:
                speak_urdu("Sir, which folder should I close?")
                folder_name = listen()
                if not folder_name:
                    speak_urdu("No folder name specified. Cancelling.")
                    return True
            else:
                speak_urdu(f"Closing folder '{folder_name}'...")

            folder_name = folder_name.lower()

            # Step 3: Close folder windows matching the name
            shell = win32com.client.Dispatch("Shell.Application")
            found = False
            for window in shell.Windows():
                try:
                    current_window_name = getattr(window, "LocationName", "").lower()
                    if folder_name in current_window_name:
                        window.Quit()
                        speak_urdu(f"Folder '{current_window_name}' closed successfully.")
                        found = True
                        break
                except:
                    continue

            if not found:
                speak_urdu(f"No open folder window found for '{folder_name}'.")

        except Exception as e:
            speak_urdu(f"Error closing folder: {e}")

        return True

    return False