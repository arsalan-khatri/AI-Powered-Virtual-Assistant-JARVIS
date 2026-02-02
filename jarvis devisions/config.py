import os
import pyttsx3
import google.generativeai as genai
import os, sys

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

# # huggingface conficuration
# import os
# from huggingface_hub import InferenceClient
# # Agar PIL install nahi hai to 'pip install pillow' karein
# # Lekin aapke pass already hai kyunki pichla code chal gaya tha
# from PIL import Image 

# # Yahan apna NAYA token dalein (Purana wala delete kar dein safety ke liye)
# HF_TOKEN = "Your API Key" 
# image_client = InferenceClient(token=HF_TOKEN)