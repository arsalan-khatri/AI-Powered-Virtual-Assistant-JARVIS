import asyncio
import edge_tts
import os

async def speak_urdu(text):
    voice = "hi-IN-MadhurNeural"   # Always works
    output = "voice_test.mp3"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)

    os.system(f"start {output}")

asyncio.run(speak_urdu("Agar chaho, mai aapke liye Jarvis ke liye full Urdu male natural voice module ready kar doon, jisme robot feel kam aur pronunciation bilkul natural ho."))
