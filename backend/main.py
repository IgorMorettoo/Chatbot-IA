import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

app = FastAPI(title="Chatbot com IA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    mensagem: str

class ChatResponse(BaseModel):
    resposta: str

@app.get("/")
def home():
    return {"status": "API do Chatbot funcionando"}

@app.post("/chat", response_model=ChatResponse)
def chat(dados: ChatRequest):
    mensagem = dados.mensagem.strip()
    if not mensagem:
        raise HTTPException(status_code=400, detail="Digite uma mensagem.")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY não configurada no arquivo .env.",
        )

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-5-mini",
            input=mensagem,
        )
        return ChatResponse(resposta=response.output_text)
    except Exception as erro:
        raise HTTPException(status_code=500, detail="Não foi possível obter uma resposta da IA no momento. Tente novamente.")
