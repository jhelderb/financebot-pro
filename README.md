# 💰 FinanceBot Pro — Consultor Financeiro com IA

> **Projeto Final — Curso de IA Generativa**  
> Chatbot especialista em finanças pessoais powered by **Groq API + Llama 3.3 70B**

---

## 📌 Sobre o Projeto

O **FinanceBot Pro** é um chatbot de Inteligência Artificial especializado em finanças pessoais que atua como um consultor financeiro virtual. Desenvolvido como projeto final do curso de IA Generativa, demonstra na prática os principais conceitos de desenvolvimento com LLMs.

### O que ele faz?
- 📊 Cria planos financeiros personalizados
- 💳 Estratégias para eliminar dívidas (bola de neve, avalanche)
- 📈 Orienta sobre investimentos (Tesouro Direto, CDB, ações, FIIs)
- 🧠 Reforma a mentalidade sobre dinheiro
- 🏆 Traça caminhos para independência financeira (FIRE)
- 📉 Ajuda a montar orçamentos e controlar gastos

### O que ele NÃO faz?
Possui **guardrails** implementados via system prompt — recusa educadamente qualquer pergunta fora do escopo financeiro.

---

## 🏗️ Arquitetura do Projeto

```
finance_chatbot/
│
├── chatbot.py           # 🤖 Core: cliente Groq + memória de conversa
├── app.py               # 🌐 Interface Web (Streamlit)
├── cli.py               # 💻 Interface Terminal (Rich)
│
├── requirements.txt     # 📦 Dependências Python
├── .env.example         # 🔑 Template de variáveis de ambiente
├── .env                 # 🔑 Suas credenciais (NÃO está no repositório)
├── teste_api.py         # 🧪 Script para validar a API
│
├── data/                # 💾 Histórico de conversas (JSON)
│   └── conversation_history.json
│
└── logs/                # 📝 Logs de interações
    └── chat_YYYY-MM-DD.log
```

---

## 🧠 Conceitos de IA Generativa Implementados

| Conceito | Implementação |
|---|---|
| **Prompt Engineering** | System prompt detalhado com persona, regras e exemplos |
| **Conversation Memory** | Buffer sliding window de 20 mensagens com persistência JSON |
| **Guardrails** | Restrições de escopo via system prompt |
| **Multi-turn Chat** | Histórico completo enviado a cada requisição |
| **Error Handling** | Tratamento tipado de RateLimitError, AuthenticationError |
| **Logging** | Todas as interações salvas em logs rotativos por dia |
| **Multi-interface** | Mesma engine, duas interfaces (Web Streamlit + CLI Rich) |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| **Python** | 3.10+ | Linguagem principal |
| **Groq SDK** | ≥ 0.11.0 | Acesso ao LLM via API |
| **Llama 3.3 70B** | — | Modelo de linguagem (via Groq) |
| **Streamlit** | ≥ 1.40.0 | Interface web interativa |
| **Rich** | ≥ 13.0.0 | Interface CLI colorida |
| **python-dotenv** | ≥ 1.0.0 | Gerenciamento de variáveis de ambiente |
| **JSON** | — | Persistência do histórico |

---

## ⚙️ Instalação e Configuração

### Pré-requisitos
- Python 3.10 ou superior
- Conta gratuita no [Groq Console](https://console.groq.com)

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/finance-chatbot.git
cd finance-chatbot
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv

# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a API Key

Obtenha sua chave **gratuita** em: https://console.groq.com/keys

```bash
cp .env.example .env
nano .env   # ou abra com qualquer editor de texto
```

Edite o arquivo `.env`:
```
GROQ_API_KEY=gsk_sua-chave-aqui
```

### 5. Valide a instalação

```bash
python3 teste_api.py
```

Você deve ver:
```
✅ Key encontrada: gsk_xxxx...xxxx
📡 Enviando mensagem de teste...
✅ RESPOSTA: API Groq funcionando!
🎉 Tudo certo! O chatbot está pronto para uso.
```

---

## ▶️ Como Executar

### Interface Web — Streamlit (Recomendado)

```bash
streamlit run app.py
```

Acesse no navegador: **http://localhost:8501**

### Interface Terminal — CLI

```bash
python3 cli.py
```

**Comandos disponíveis no CLI:**

| Comando | Ação |
|---|---|
| `ajuda` | Mostra os comandos disponíveis |
| `limpar` | Limpa o histórico da conversa |
| `sessao` | Exibe resumo da sessão atual |
| `sair` | Encerra o bot |

---

## 💬 Exemplos de Uso

**Orçamento pessoal:**
```
Você: Ganho R$ 4.000 por mês, pago R$ 900 de aluguel e R$ 300 de financiamento. Me ajuda a criar um orçamento.
Bot:  [Cria orçamento detalhado com a regra 50/30/20 adaptado à sua realidade]
```

**Estratégia de dívidas:**
```
Você: Tenho R$ 5.000 no cartão (juros 12% a.m.) e R$ 8.000 de empréstimo (3% a.m.). Por onde começo?
Bot:  [Estratégia avalanche com ordem de pagamento e projeção de quitação]
```

**Investimentos para iniciantes:**
```
Você: Consigo guardar R$ 300 por mês. Qual o melhor investimento para começar?
Bot:  [Plano progressivo: reserva de emergência → Tesouro Direto → CDB → diversificação]
```

**Guardrail em ação:**
```
Você: Me fala sobre a última Copa do Mundo.
Bot:  Esse tema está fora da minha área de especialização 😊. Sou focado exclusivamente em finanças pessoais...
```

---

## 🔑 Informações sobre a API Groq

| Item | Detalhe |
|---|---|
| **Custo** | 100% gratuito |
| **Cartão de crédito** | Não necessário |
| **Restrição geográfica** | Nenhuma — funciona no Brasil |
| **Modelo utilizado** | `llama-3.3-70b-versatile` |
| **Limite free** | ~14.400 tokens/minuto |
| **Onde obter a chave** | https://console.groq.com/keys |

---

## 📁 Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `GROQ_API_KEY` | ✅ Sim | Chave de acesso à API Groq |

---

## ⚠️ Aviso Legal

Este chatbot é uma ferramenta **educacional**. As orientações fornecidas são de caráter informativo e **não substituem** a consultoria de um profissional certificado (CFP — Certified Financial Planner). Para decisões financeiras importantes, consulte sempre um especialista habilitado.

---

## 📄 Licença

Projeto educacional desenvolvido como trabalho final do Curso de IA Generativa.
