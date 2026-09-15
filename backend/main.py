import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai


# ============================================================
# CONFIGURAÇÃO
# ============================================================

load_dotenv()

app = FastAPI(
    title="Chatbot IA",
    description="API de chatbot utilizando FastAPI + Gemini",
    version="1.0.0"
)


# ============================================================
# CORS - PERMITE COMUNICAÇÃO COM O REACT
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# CONFIGURAÇÃO DA API GEMINI
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY não encontrada. "
        "Verifique se o arquivo .env está dentro da pasta backend."
    )

client = genai.Client(api_key=api_key)


# ============================================================
# MODELOS DE DADOS
# ============================================================

class MensagemRequest(BaseModel):
    mensagem: str


class MensagemResponse(BaseModel):
    resposta: str


# ============================================================
# ROTA DE TESTE
# ============================================================

@app.get("/")
def inicio():
    return {
        "status": "online",
        "mensagem": "API do Chatbot funcionando!"
    }


# ============================================================
# ROTA DO CHAT
# ============================================================

@app.post("/chat", response_model=MensagemResponse)
def chat(dados: MensagemRequest):

    mensagem = dados.mensagem.strip()

    if not mensagem:
        raise HTTPException(
            status_code=400,
            detail="Digite uma mensagem."
        )

    try:

        resposta = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=mensagem
        )

        if not resposta.text:
            raise HTTPException(
                status_code=500,
                detail="A Inteligência Artificial não retornou uma resposta."
            )

        return MensagemResponse(
            resposta=resposta.text
        )

    except HTTPException:
        raise

    except Exception as erro:

        # Mostra o erro verdadeiro no terminal
        print("\n")
        print("==========================================")
        print("ERRO AO CONSULTAR GEMINI")
        print("==========================================")
        print(repr(erro))
        print("==========================================")
        print("\n")

        # Temporariamente mostra o erro também no frontend
        # para conseguirmos descobrir o problema.
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao consultar a IA: {str(erro)}"
        )


# ============================================================
# EXECUÇÃO DIRETA
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )