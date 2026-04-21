"""
╔══════════════════════════════════════════════════════════════╗
║          CONSULTOR FINANCEIRO IA - FinanceBot Pro            ║
║          Projeto Final - Curso de IA Generativa              ║
║          Motor: Groq API — Llama 3.3 70B (GRATUITO)         ║
╚══════════════════════════════════════════════════════════════╝

Descrição:
    Chatbot especialista em finanças pessoais usando a API Groq,
    que oferece acesso GRATUITO e sem restrição geográfica ao
    modelo Llama 3.3 70B — um dos melhores modelos open-source.

Autor: Projeto Final IA Generativa
Versão: 5.0.0 — Groq Edition
"""

import os, json, time, datetime, logging
from pathlib import Path
from typing import Optional
from groq import Groq, RateLimitError, AuthenticationError, APIConnectionError

# ── Logging ──────────────────────────────────────────────────
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"chat_{datetime.date.today()}.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("FinanceBot")

# ── Configurações ─────────────────────────────────────────────
MODEL       = "llama-3.3-70b-versatile"   # melhor modelo gratuito do Groq
MAX_HISTORY = 20                           # máximo de pares no buffer
HISTORY_FILE = Path("data/conversation_history.json")

# ── System Prompt ─────────────────────────────────────────────
SYSTEM_PROMPT = """Você é o FinanceBot Pro, um consultor financeiro pessoal altamente especializado e empático. Responda SEMPRE em português brasileiro. Seu objetivo é transformar a vida financeira das pessoas de forma prática e humana.

## SUA ESPECIALIDADE
- Planejamento financeiro pessoal: orçamentos, metas de curto/médio/longo prazo
- Eliminação de dívidas: métodos bola de neve, avalanche, negociação com credores
- Investimentos: Tesouro Direto, CDB, LCI/LCA, ações, FIIs, previdência privada
- Mentalidade financeira: comportamento com dinheiro, vieses cognitivos
- Renda extra: empreendedorismo, freelance, fontes de renda passiva
- Aposentadoria e independência financeira: FIRE, regra dos 4%
- Impostos e IR: tributação de investimentos no Brasil

## ESTILO DE COMUNICAÇÃO
- Linguagem clara, acolhedora e motivadora — sem jargões desnecessários
- Seja empático: muitas pessoas têm vergonha de falar sobre dívidas
- Use dados concretos, cálculos e exemplos numéricos em Reais (R$)
- Dê sempre um próximo passo prático e acionável ao final
- Use emojis moderadamente (💰📊💡)
- Use tabelas e listas em Markdown quando relevante

## GUARDRAILS — REGRAS ABSOLUTAS
RECUSE qualquer pergunta fora de finanças (saúde, política, entretenimento, culinária, etc.).
Resposta padrão para fora do escopo:
"Esse tema está fora da minha área de especialização 😊. Sou focado exclusivamente em finanças pessoais. Posso te ajudar com [sugira tema financeiro relevante]?"

## DISCLAIMER
Para recomendações de investimento sempre inclua:
⚠️ Esta é uma orientação educacional. Consulte um assessor financeiro certificado (CFP) para decisões importantes.
"""

# ── Memória de Conversa ───────────────────────────────────────
class ConversationMemory:
    """
    Gerencia histórico da conversa com persistência em JSON.
    Formato OpenAI-compatible (usado pelo Groq):
        [{"role": "user", "content": "..."},
         {"role": "assistant", "content": "..."}, ...]
    """

    def __init__(self, max_messages: int = MAX_HISTORY):
        self.max_messages = max_messages
        self.messages: list[dict] = []
        HISTORY_FILE.parent.mkdir(exist_ok=True)
        self._load()

    def _load(self):
        if HISTORY_FILE.exists():
            try:
                data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
                self.messages = data.get("messages", [])
                logger.info(f"Histórico carregado: {len(self.messages)} mensagens")
            except Exception:
                self.messages = []

    def save(self):
        HISTORY_FILE.write_text(
            json.dumps({
                "saved_at": datetime.datetime.now().isoformat(),
                "messages": self.messages
            }, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def add(self, role: str, content: str):
        """role: 'user' ou 'assistant'"""
        self.messages.append({"role": role, "content": content})
        # Sliding window — mantém só as últimas N mensagens
        if len(self.messages) > self.max_messages * 2:
            self.messages = self.messages[-(self.max_messages * 2):]
        self.save()

    def pop_last(self):
        """Remove última mensagem em caso de erro."""
        if self.messages:
            self.messages.pop()

    def get_messages_for_api(self) -> list[dict]:
        """
        Retorna histórico completo no formato Groq/OpenAI,
        incluindo o system prompt no início.
        """
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            *self.messages
        ]

    def clear(self):
        self.messages = []
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        logger.info("Histórico limpo.")


# ── Cliente Principal ─────────────────────────────────────────
class FinanceBotClient:
    """
    Cliente Groq para o FinanceBot Pro.
    A API Groq é compatível com o formato OpenAI e oferece
    acesso GRATUITO ao Llama 3.3 70B sem restrição geográfica.
    """

    def __init__(self, api_key: Optional[str] = None):
        key = api_key or os.environ.get("GROQ_API_KEY")
        if not key:
            raise ValueError(
                "API Key não encontrada!\n"
                "Configure no .env: GROQ_API_KEY=sua-chave\n"
                "Chave GRATUITA em: https://console.groq.com/keys"
            )
        self.client = Groq(api_key=key)
        self.memory = ConversationMemory()
        logger.info(f"FinanceBotClient (Groq) iniciado — modelo: {MODEL}")

    def chat(self, user_message: str) -> str:
        """
        Envia mensagem e retorna resposta do modelo.
        Inclui retry automático com backoff para rate limit.
        """
        logger.info(f"USER: {user_message[:100]}")
        self.memory.add("user", user_message)

        for tentativa in range(3):
            try:
                logger.info(f"Tentativa {tentativa+1}/3 — chamando Groq API...")

                completion = self.client.chat.completions.create(
                    model=MODEL,
                    messages=self.memory.get_messages_for_api(),
                    max_tokens=1500,
                    temperature=0.7,
                )

                reply = completion.choices[0].message.content
                logger.info(f"RESPOSTA OK ({len(reply)} chars)")
                self.memory.add("assistant", reply)
                return reply

            except RateLimitError as e:
                logger.warning(f"RateLimitError tentativa {tentativa+1}: {str(e)[:100]}")
                if tentativa < 2:
                    espera = (tentativa + 1) * 10
                    logger.info(f"Aguardando {espera}s...")
                    time.sleep(espera)
                    continue
                self.memory.pop_last()
                return (
                    "⚠️ **Limite temporário atingido.**\n\n"
                    "Aguarde 30 segundos e tente novamente.\n"
                    "_(O plano free do Groq é generoso — isso raramente acontece)_"
                )

            except AuthenticationError:
                logger.error("AuthenticationError — API Key inválida")
                self.memory.pop_last()
                return "❌ **API Key inválida.** Verifique sua chave em console.groq.com/keys"

            except APIConnectionError:
                logger.error("APIConnectionError — sem conexão")
                if tentativa < 2:
                    time.sleep(5)
                    continue
                self.memory.pop_last()
                return "❌ **Sem conexão com a internet.** Verifique sua rede."

            except Exception as e:
                import traceback
                logger.error(f"Erro inesperado:\n{traceback.format_exc()}")
                if tentativa < 2:
                    time.sleep(3)
                    continue
                self.memory.pop_last()
                return f"❌ **Erro inesperado:** {type(e).__name__}: {str(e)[:200]}"

        self.memory.pop_last()
        return "⚠️ Não foi possível obter resposta. Tente novamente."

    def clear_history(self):
        self.memory.clear()
