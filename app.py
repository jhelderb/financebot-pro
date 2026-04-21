"""
╔══════════════════════════════════════════════════════════════╗
║          INTERFACE WEB - FinanceBot Pro                      ║
║          Streamlit App - Consultor Financeiro IA             ║
╚══════════════════════════════════════════════════════════════╝

Interface web interativa construída com Streamlit.
Execute com: streamlit run app.py
"""

import streamlit as st
import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

from chatbot import FinanceBotClient  # Motor: Google Gemini

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FinanceBot Pro | Consultor Financeiro IA",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS CUSTOMIZADO — VISUAL REFINADO
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

    /* Tema escuro elegante */
    :root {
        --bg-primary: #0a0f1e;
        --bg-secondary: #0f1729;
        --bg-card: #141d35;
        --accent-gold: #d4a843;
        --accent-green: #2ecc87;
        --accent-red: #e74c6a;
        --text-primary: #e8eaf2;
        --text-secondary: #8892b0;
        --border: rgba(212, 168, 67, 0.2);
    }

    /* Background geral */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0d1526 50%, #0a1520 100%);
        font-family: 'DM Sans', sans-serif;
    }

    /* Esconde elementos default do Streamlit */
    #MainMenu, footer, header { visibility: hidden; }

    /* Header customizado */
    .finance-header {
        background: linear-gradient(90deg, rgba(212,168,67,0.1) 0%, rgba(46,204,135,0.05) 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .finance-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(ellipse at 20% 50%, rgba(212,168,67,0.05) 0%, transparent 60%);
        pointer-events: none;
    }
    .finance-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: var(--accent-gold);
        margin: 0;
        letter-spacing: -0.5px;
    }
    .finance-header p {
        color: var(--text-secondary);
        margin: 6px 0 0 0;
        font-size: 0.95rem;
        font-weight: 300;
    }

    /* Mensagens do chat */
    .msg-user {
        background: linear-gradient(135deg, rgba(212,168,67,0.12), rgba(212,168,67,0.06));
        border: 1px solid rgba(212,168,67,0.25);
        border-radius: 16px 16px 4px 16px;
        padding: 14px 18px;
        margin: 10px 0 10px 60px;
        color: var(--text-primary);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .msg-bot {
        background: rgba(15, 23, 41, 0.8);
        border: 1px solid rgba(46,204,135,0.2);
        border-radius: 16px 16px 16px 4px;
        padding: 14px 18px;
        margin: 10px 60px 10px 0;
        color: var(--text-primary);
        font-size: 0.95rem;
        line-height: 1.7;
    }
    .msg-label-user {
        text-align: right;
        font-size: 0.75rem;
        color: var(--accent-gold);
        margin-bottom: 4px;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .msg-label-bot {
        font-size: 0.75rem;
        color: var(--accent-green);
        margin-bottom: 4px;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }

    /* Input de texto */
    .stTextInput > div > div > input,
    .stChatInput textarea {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stChatInput textarea:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 2px rgba(212,168,67,0.15) !important;
    }

    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-gold), #b8922e) !important;
        color: #0a0f1e !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        padding: 8px 20px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(212,168,67,0.3) !important;
    }

    /* Cards de métricas */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: var(--accent-gold);
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.78rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 4px;
    }

    /* Sugestões rápidas */
    .suggestion-btn {
        background: rgba(46,204,135,0.08) !important;
        border: 1px solid rgba(46,204,135,0.25) !important;
        color: var(--accent-green) !important;
        border-radius: 20px !important;
        font-size: 0.82rem !important;
        padding: 6px 14px !important;
    }

    /* Welcome card */
    .welcome-card {
        background: linear-gradient(135deg, rgba(46,204,135,0.08), rgba(212,168,67,0.05));
        border: 1px solid rgba(46,204,135,0.2);
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
    }

    /* Scrollbar personalizada */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
# INICIALIZAÇÃO DO ESTADO DA SESSÃO
# ─────────────────────────────────────────────
def init_session_state():
    """Inicializa todas as variáveis de estado da sessão Streamlit."""
    if "bot" not in st.session_state:
        api_key = os.environ.get("GROQ_API_KEY", "")
        if api_key:
            try:
                st.session_state.bot = FinanceBotClient(api_key=api_key)
                st.session_state.bot_ready = True
            except Exception:
                st.session_state.bot = None
                st.session_state.bot_ready = False
        else:
            st.session_state.bot = None
            st.session_state.bot_ready = False

    if "chat_display" not in st.session_state:
        st.session_state.chat_display = []  # lista de {role, content, time}

    if "message_count" not in st.session_state:
        st.session_state.message_count = 0

    if "session_start" not in st.session_state:
        st.session_state.session_start = datetime.datetime.now()


init_session_state()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 10px 0 20px 0;'>
            <div style='font-size:3rem;'>💰</div>
            <div style='font-family:"Playfair Display",serif; font-size:1.3rem;
                        color:#d4a843; font-weight:700;'>FinanceBot Pro</div>
            <div style='font-size:0.78rem; color:#8892b0; margin-top:4px;'>Consultor Financeiro IA</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Configuração da API Key ──
    st.markdown("**⚙️ Configuração**")

    if not st.session_state.bot_ready:
        api_input = st.text_input(
            "🔑 Gemini API Key",
            type="password",
            placeholder="gsk_...",
            help="Obtenha GRÁTIS em console.groq.com/keys",
        )
        if st.button("✅ Conectar", use_container_width=True):
            if api_input:
                try:
                    st.session_state.bot = FinanceBotClient(api_key=api_input)
                    st.session_state.bot_ready = True
                    st.success("Conectado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")
            else:
                st.warning("Insira uma API Key válida.")
    else:
        st.success("✅ API Conectada")
        if st.button("🔌 Desconectar", use_container_width=True):
            st.session_state.bot = None
            st.session_state.bot_ready = False
            st.rerun()

    st.divider()

    # ── Métricas da sessão ──
    st.markdown("**📊 Sessão Atual**")
    elapsed = datetime.datetime.now() - st.session_state.session_start
    minutes = int(elapsed.total_seconds() / 60)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""<div class='metric-card'>
                <div class='metric-value'>{st.session_state.message_count}</div>
                <div class='metric-label'>Mensagens</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""<div class='metric-card'>
                <div class='metric-value'>{minutes}m</div>
                <div class='metric-label'>Duração</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Tópicos de ajuda ──
    st.markdown("**💡 Posso te ajudar com:**")
    topics = [
        "📋 Plano de orçamento mensal",
        "💳 Sair das dívidas",
        "📈 Começar a investir",
        "🧠 Mentalidade financeira",
        "🏠 Financiamento imobiliário",
        "💼 Renda extra e freelance",
        "🎯 Independência financeira",
        "📊 Análise de gastos",
    ]
    for topic in topics:
        st.markdown(
            f"<div style='font-size:0.83rem; color:#8892b0; padding:3px 0;'>{topic}</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Ações ──
    if st.button("🗑️ Limpar Conversa", use_container_width=True):
        st.session_state.chat_display = []
        st.session_state.message_count = 0
        if st.session_state.bot_ready:
            st.session_state.bot.clear_history()
        st.rerun()

    st.markdown(
        "<div style='font-size:0.72rem; color:#4a5568; text-align:center; margin-top:20px;'>"
        "🤖 Motor: Groq — Llama 3.3 70B (free)<br>"
        "⚠️ Não substitui consultoria financeira profissional</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# CONTEÚDO PRINCIPAL
# ─────────────────────────────────────────────

# Header
st.markdown(
    """
    <div class='finance-header'>
        <h1>💰 FinanceBot Pro</h1>
        <p>Seu consultor financeiro pessoal movido por Inteligência Artificial · Groq — Llama 3.3 70B · Projeto Final IA Generativa</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Se não conectado, mostra tela de boas vindas
if not st.session_state.bot_ready:
    st.markdown(
        """
        <div class='welcome-card'>
            <h3 style='font-family:"Playfair Display",serif; color:#2ecc87; margin:0 0 12px 0;'>
                👋 Bem-vindo ao FinanceBot Pro!
            </h3>
            <p style='color:#8892b0; margin:0 0 16px 0; line-height:1.7;'>
                Sou um consultor financeiro virtual treinado para ajudar você a transformar
                sua vida financeira. Posso criar planos de orçamento, estratégias para eliminar
                dívidas, orientações sobre investimentos e muito mais.
            </p>
            <p style='color:#d4a843; font-size:0.9rem; margin:0;'>
                👈 Configure sua <strong>API Key da Anthropic</strong> na barra lateral para começar.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### O que posso fazer por você?")
    cols = st.columns(3)
    features = [
        ("💸", "Plano Financeiro", "Crio um plano personalizado baseado na sua renda e gastos reais"),
        ("🎯", "Eliminar Dívidas", "Estratégias comprovadas: método bola de neve e avalanche"),
        ("📈", "Investimentos", "Onde colocar seu dinheiro de acordo com seu perfil e objetivos"),
        ("🧠", "Mentalidade", "Reforma completa da sua relação com o dinheiro"),
        ("🏆", "FIRE", "Caminho para a independência financeira e aposentadoria antecipada"),
        ("📊", "Orçamento 50/30/20", "Aprenda a distribuir sua renda de forma inteligente"),
    ]
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"""<div class='metric-card' style='margin-bottom:16px; text-align:left;'>
                    <div style='font-size:1.8rem; margin-bottom:8px;'>{icon}</div>
                    <div style='font-family:"Playfair Display",serif; color:#d4a843;
                                font-size:1rem; margin-bottom:6px;'>{title}</div>
                    <div style='font-size:0.82rem; color:#8892b0; line-height:1.5;'>{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )
    st.stop()

# ── Área de chat ──
chat_container = st.container()

# Mensagem inicial se chat vazio
if not st.session_state.chat_display:
    with chat_container:
        st.markdown(
            """
            <div class='welcome-card'>
                <div style='font-size:1.5rem; margin-bottom:8px;'>👋</div>
                <div style='font-family:"Playfair Display",serif; color:#2ecc87;
                            font-size:1.1rem; margin-bottom:8px;'>
                    Olá! Sou o FinanceBot Pro.
                </div>
                <div style='color:#8892b0; font-size:0.92rem; line-height:1.7;'>
                    Estou aqui para transformar sua vida financeira. Pode me contar sua situação atual,
                    fazer perguntas sobre investimentos, dívidas, orçamento — ou simplesmente
                    dizer "Quero organizar minhas finanças" para começarmos do zero. 💰
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Sugestões rápidas
    st.markdown("**🚀 Começar com:**")
    suggestions = [
        "Quero sair das dívidas, por onde começo?",
        "Como montar um orçamento com meu salário?",
        "Qual o melhor investimento para iniciantes?",
        "Como atingir a independência financeira?",
        "Me explique a regra 50/30/20",
    ]
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state._quick_input = suggestion
                st.rerun()

# Exibe histórico do chat
with chat_container:
    for msg in st.session_state.chat_display:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='msg-label-user'>Você · {msg['time']}</div>"
                f"<div class='msg-user'>{msg['content']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='msg-label-bot'>💰 FinanceBot Pro · {msg['time']}</div>"
                f"<div class='msg-bot'>{msg['content']}</div>",
                unsafe_allow_html=True,
            )


# ── Input do usuário ──
user_input = st.chat_input("Faça sua pergunta financeira aqui... 💬")

# Processa sugestão rápida
if hasattr(st.session_state, "_quick_input") and st.session_state._quick_input:
    user_input = st.session_state._quick_input
    st.session_state._quick_input = None

# Processa mensagem
if user_input and user_input.strip():
    now = datetime.datetime.now().strftime("%H:%M")

    # Adiciona ao display
    st.session_state.chat_display.append(
        {"role": "user", "content": user_input, "time": now}
    )
    st.session_state.message_count += 1

    # Gera resposta
    with st.spinner("💭 Analisando sua situação financeira..."):
        response = st.session_state.bot.chat(user_input)

    # Adiciona resposta ao display
    st.session_state.chat_display.append(
        {"role": "assistant", "content": response, "time": now}
    )

    st.rerun()
