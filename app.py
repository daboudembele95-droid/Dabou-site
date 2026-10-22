from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import requests
import os
from groq import Groq
from TTS.api import TTS

app = FastAPI()

# Autoriser Flutter à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 1. CLES API =====
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)

print("Chargement TTS... 1ere fois sera lent")
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

SYSTEM_PROMPT = """
I ye mɔgɔ ye i tɔgɔ ko Bambara AI. I bɛ kuma Bambara kelen. 
I ka kuma ni mɔgɔw bɛ kuma cogo min na Bamako. I ka kuma surunya. 
I kana kuma franse walima anglais.
"""

@app.post("/chat")
async def chat(audio: UploadFile = File(...)):
    try:
        # 1. STT Groq
        audio_bytes = await audio.read()
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes),
            model="whisper-large-v3"
        )
        texte_utilisateur = transcription.text

        # 2. LLM Together
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
            json={
                "model": "Qwen/Qwen2-7B-Instruct",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": texte_utilisateur}],
                "max_tokens": 200
            }
        )
        reponse_texte = response.json()['choices'][0]['message']['content']

        # 3. TTS
        audio_buffer = io.BytesIO()
        tts.tts_to_file(text=reponse_texte, speaker="Ana", language="fr", file_path=audio_buffer)
        audio_buffer.seek(0)
        
        return StreamingResponse(audio_buffer, media_type="audio/wav")

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "Bambara Voice API est en ligne 🇲🇱"}