"""
Teste rápido da API Groq.
Execute: python3 teste_api.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

from groq import Groq, AuthenticationError, RateLimitError

key = os.environ.get("GROQ_API_KEY", "")
if not key:
    print("❌ GROQ_API_KEY não encontrada no .env")
    exit(1)

print(f"✅ Key encontrada: {key[:8]}...{key[-4:]}")
client = Groq(api_key=key)

try:
    print("📡 Enviando mensagem de teste...")
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente financeiro."},
            {"role": "user",   "content": "Responda apenas: API Groq funcionando!"}
        ],
        max_tokens=50,
    )
    print(f"✅ RESPOSTA: {resp.choices[0].message.content}")
    print("\n🎉 Tudo certo! O chatbot está pronto para uso.")

except AuthenticationError:
    print("❌ API Key inválida. Verifique em console.groq.com/keys")
except RateLimitError:
    print("⚠️ Rate limit — aguarde 30s e tente novamente.")
except Exception as e:
    print(f"❌ Erro: {type(e).__name__}: {e}")
