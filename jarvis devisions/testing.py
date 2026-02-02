import requests
import os
import random
import time

# --- CONFIGURATION ---
FOLDER_PATH = r"C:\Users\Arsalan Khatri\Desktop\jarvis devisions\generated_images"

def test_image_generation(prompt):
    print(f"\n🎨 Processing Prompt: '{prompt}'")
    
    # --- QUALITY FIX: Smooth & Clean Prompt ---
    # 'smooth', 'clean lines', 'denoise' add kiya hai taake pixels na phatein
    enhanced_prompt = f"{prompt}, hyper-realistic, 8k resolution, cinematic lighting, sharp focus, smooth texture, clean lines, unreal engine 5 render, masterpiece"
    
    # --- MODEL LIST (Backup Plan) ---
    # Agar pehla fail hua, to dusra try karega
    models = ["flux-realism", "flux-pro", "flux", "turbo"]
    
    # Folder Check
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    # Random Seed
    seed = random.randint(1, 10000000)

    # Loop through models
    for model_name in models:
        print(f"🔄 Trying Model: {model_name}...")
        
        try:
            # URL Construction
            url = f"https://pollinations.ai/p/{enhanced_prompt}?width=1024&height=1024&seed={seed}&model={model_name}&nologo=true"
            
            # Request
            response = requests.get(url, timeout=40)
            
            if response.status_code == 200:
                # --- SUCCESS ---
                print(f"✅ Success! Image generated using '{model_name}'")
                
                # Numbering Logic
                counter = 1
                while True:
                    filename = f"jarvis_{counter}.jpg"
                    final_path = os.path.join(FOLDER_PATH, filename)
                    if os.path.exists(final_path):
                        counter += 1
                    else:
                        break
                
                # Save
                with open(final_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"📍 Saved at: {final_path}")
                os.startfile(final_path)
                
                # Loop tod do kyunke kaam ho gaya
                return 
            
            else:
                print(f"⚠️ Model '{model_name}' failed (Status: {response.status_code}). Switching to next...")
                
        except Exception as e:
            print(f"❌ Error with {model_name}: {e}")
            continue # Agle model par jao

    print("❌ Sorry Sir, sare models try kiye magar server down hai.")

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("--- JARVIS SMART IMAGE GENERATOR ---")
    while True:
        print("\n" + "="*50)
        user_input = input("Enter Prompt (or 'exit'): ")
        
        if user_input.lower() in ['exit', 'quit']:
            break
            
        if user_input.strip() != "":
            test_image_generation(user_input)