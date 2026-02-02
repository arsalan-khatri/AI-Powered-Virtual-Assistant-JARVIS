import os, sys
from utils import speak_urdu, listen, chat_with_gemini,get_ai_startup_message
from commands import execute_system_command



# --- MAIN LOOP ---
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------------------")
    print("   JARVIS AI ASSISTANT ONLINE   ")
    print("--------------------------------")

    # speak_urdu("Hello sir, I am online and listening.")
    # Ab (LLM wala tareeqa):
    
    greeting_text = get_ai_startup_message() # Gemini se text mangwaya
    speak_urdu(greeting_text)

    while True:
        user_command = listen()
        if user_command:
            print(f"You:    {user_command}")

            if "exit" in user_command.lower() or "stop" in user_command.lower() or "bye" in user_command.lower():
                speak_urdu("System shutting down. Goodbye.")
                sys.exit()

            if not execute_system_command(user_command):
                response = chat_with_gemini(user_command)
                speak_urdu(response)

            print("-" * 30)
