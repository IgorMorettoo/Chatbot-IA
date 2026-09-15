import { FormEvent, useState } from 'react'

type Mensagem = {
  autor: 'usuario' | 'ia'
  texto: string
}

function App() {
  const [texto, setTexto] = useState('')
  const [mensagens, setMensagens] = useState<Mensagem[]>([
    { autor: 'ia', texto: 'Olá! Sou seu chatbot com Inteligência Artificial. Como posso ajudar?' },
  ])
  const [carregando, setCarregando] = useState(false)

  async function enviarMensagem(event: FormEvent) {
    event.preventDefault()
    const pergunta = texto.trim()
    if (!pergunta || carregando) return

    setMensagens((atual) => [...atual, { autor: 'usuario', texto: pergunta }])
    setTexto('')
    setCarregando(true)

    try {
      const resposta = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensagem: pergunta }),
      })

      const dados = await resposta.json()
      if (!resposta.ok) throw new Error(dados.detail || 'Erro ao consultar a IA.')

      setMensagens((atual) => [...atual, { autor: 'ia', texto: dados.resposta }])
    } catch (erro) {
      const mensagemErro = erro instanceof Error ? erro.message : 'Erro inesperado.'
      setMensagens((atual) => [...atual, { autor: 'ia', texto: `Erro: ${mensagemErro}` }])
    } finally {
      setCarregando(false)
    }
  }

  return (
    <main className="pagina">
      <section className="chat">
        <header>
          <div className="icone">AI</div>
          <div>
            <h1>Chatbot IA</h1>
            <p>React + FastAPI + Inteligência Artificial</p>
          </div>
        </header>

        <div className="mensagens">
          {mensagens.map((mensagem, indice) => (
            <div key={indice} className={`linha ${mensagem.autor}`}>
              <div className="balao">{mensagem.texto}</div>
            </div>
          ))}
          {carregando && <div className="digitando">IA está respondendo...</div>}
        </div>

        <form onSubmit={enviarMensagem}>
          <input
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            placeholder="Digite sua mensagem..."
            disabled={carregando}
          />
          <button type="submit" disabled={carregando || !texto.trim()}>
            Enviar
          </button>
        </form>
      </section>
    </main>
  )
}

export default App
