from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from groq import Groq

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = "I ye mɔgɔ ye i tɔgɔ ko Bambara AI. I bɛ kuma Bambara kelen. I ka kuma ni mɔgɔw bɛ kuma cogo min na Bamako. I ka kuma surunya."

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
            json={"model": "Qwen/Qwen2-7B-Instruct", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": texte_utilisateur}], "max_tokens": 200}
        )
        reponse_texte = response.json()['choices'][0]['message']['content']

        return JSONResponse({"texte_utilisateur": texte_utilisateur, "reponse_ia": reponse_texte})

    except Exception as e:
        return JSONResponse({"error": str(e)})

@app.get("/")
def home():
    return {"message": "Bambara Voice API V1 Texte 🇲🇱"}