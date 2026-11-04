
import os
import whisper
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save

# Load API key
load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not API_KEY:
    raise ValueError("ElevenLabs API key not found!")

# Initialize AI services
print("Loading speech recognition model...")
model = whisper.load_model("base")

client = ElevenLabs(api_key=API_KEY)

# Input audio file
input_file = "input_voice.mp3"

if not os.path.exists(input_file):
    raise FileNotFoundError("Input audio file not found!")

# Step 1: Convert speech into text
print("\nConverting voice into text...")

result = model.transcribe(input_file)
recognized_text = result["text"]

print("\nRecognized Text:")
print(recognized_text)

# Step 2: Generate AI voice
print("\nGenerating AI voice...")

audio = client.text_to_speech.convert(
    text=recognized_text,
    voice_id="EXAVITQu4vr4xnSDxMaL",
    model_id="eleven_multilingual_v2"
)

# Step 3: Save generated audio
save(audio, "ai_voice.mp3")

print("\nVoice conversion completed!")
print("Output saved as ai_voice.mp3")
