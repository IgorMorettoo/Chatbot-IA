# Chatbot com Inteligência Artificial

Projeto acadêmico com frontend React + TypeScript, backend FastAPI e integração com API de IA.

## 1. Backend

Abra um terminal na pasta `backend`:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e informe sua chave:

```env
OPENAI_API_KEY=sua_chave_aqui
```

Inicie a API:

```bash
uvicorn main:app --reload
```

Backend: `http://localhost:8000`

## 2. Frontend

Em outro terminal, abra a pasta `frontend`:

```bash
npm install
npm run dev
```

Abra no navegador o endereço exibido pelo Vite (normalmente `http://localhost:5173`).

## Importante

Nunca envie o arquivo `backend/.env` para o GitHub. O `.gitignore` já está configurado para ignorá-lo.
