"""
╔══════════════════════════════════════════════════════════════╗
║          INTERFACE CLI - FinanceBot Pro                      ║
║          Terminal com Rich - Consultor Financeiro IA         ║
║          Motor: Groq API — Llama 3.3 70B (GRATUITO)         ║
╚══════════════════════════════════════════════════════════════╝

Interface de terminal rica usando a biblioteca Rich.
Execute com: python3 cli.py
"""

import os
import sys
import datetime
from dotenv import load_dotenv

load_dotenv()

# ─── Verifica dependências ───────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.prompt import Prompt
    from rich.rule import Rule
except ImportError:
    print("❌ Dependência ausente. Execute: pip install rich")
    sys.exit(1)

from chatbot import FinanceBotClient

console = Console()

BANNER = """
 ███████╗██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗
 ██╔════╝██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██╔════╝
 █████╗  ██║██╔██╗ ██║███████║██╔██╗ ██║██║     █████╗  
 ██╔══╝  ██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██╔══╝  
 ██║     ██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗███████╗
 ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝
                  💰  B O T   P R O  💰
          Consultor Financeiro Pessoal com IA
        Motor: Groq API · Llama 3.3 70B (Gratuito)
"""

HELP_TEXT = """
**Comandos disponíveis:**
- `sair` / `exit` — Encerrar o bot
- `limpar` / `clear` — Limpar histórico da conversa
- `ajuda` / `help` — Mostrar esta mensagem
- `sessao` — Ver resumo da sessão atual

**Tópicos que posso ajudar:**
💸 Orçamento e controle de gastos
💳 Estratégias para eliminar dívidas
📈 Introdução a investimentos
🧠 Mentalidade e comportamento financeiro
🏆 Independência financeira / FIRE
🏠 Financiamento e imóveis
💼 Renda extra e freelance
"""


def print_banner():
    console.print(BANNER, style="bold gold1")
    console.print(
        Panel(
            "[dim]Seu consultor financeiro pessoal movido por IA · Groq · Llama 3.3 70B[/dim]",
            border_style="gold1",
            padding=(0, 2),
        )
    )
    console.print()


def print_welcome():
    console.print(
        Panel(
            "👋 [bold green]Olá! Sou o FinanceBot Pro.[/bold green]\n\n"
            "[dim]Estou aqui para transformar sua vida financeira. Me conte sua situação,\n"
            "faça perguntas sobre dívidas, investimentos, orçamento ou simplesmente diga\n"
            "[bold]'Quero organizar minhas finanças'[/bold] para começarmos!\n\n"
            "Digite [bold]ajuda[/bold] para ver os comandos disponíveis.[/dim]",
            title="[gold1]💰 FinanceBot Pro[/gold1]",
            border_style="green",
            padding=(1, 2),
        )
    )
    console.print()


def format_response(text: str) -> Panel:
    """Formata a resposta do bot como um painel rico com Markdown."""
    return Panel(
        Markdown(text),
        title="[green]💰 FinanceBot Pro[/green]",
        border_style="green",
        padding=(1, 2),
    )


def main():
    print_banner()

    # Verifica API Key
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        console.print(
            Panel(
                "⚠️ [bold yellow]API Key não encontrada![/bold yellow]\n\n"
                "Configure com:\n"
                "[bold cyan]export GROQ_API_KEY='sua-chave-aqui'[/bold cyan]\n\n"
                "Ou crie um arquivo [bold].env[/bold] com:\n"
                "[bold cyan]GROQ_API_KEY=sua-chave-aqui[/bold cyan]\n\n"
                "Chave GRATUITA em:\n"
                "[bold green]https://console.groq.com/keys[/bold green]",
                border_style="yellow",
                padding=(1, 2),
            )
        )
        sys.exit(1)

    # Inicializa o bot
    try:
        bot = FinanceBotClient(api_key=api_key)
        console.print("[dim green]✅ API Groq conectada com sucesso[/dim green]\n")
    except Exception as e:
        console.print(f"[bold red]❌ Erro ao inicializar: {e}[/bold red]")
        sys.exit(1)

    print_welcome()

    # Stats da sessão
    session_start = datetime.datetime.now()
    message_count = 0

    # Loop principal
    while True:
        try:
            console.print(Rule(style="dim"))
            user_input = Prompt.ask("[bold gold1]Você[/bold gold1]").strip()

            if not user_input:
                continue

            cmd = user_input.lower()

            # ── Comandos especiais ──────────────────────────
            if cmd in ("sair", "exit", "quit", "q"):
                elapsed = datetime.datetime.now() - session_start
                console.print(
                    Panel(
                        f"👋 Até logo! Sessão de [bold]{int(elapsed.total_seconds()/60)}[/bold] minutos.\n"
                        f"[dim]{message_count} mensagens trocadas.[/dim]\n\n"
                        "[green]Continue aplicando os conselhos financeiros! Você consegue! 💪[/green]",
                        border_style="gold1",
                        padding=(1, 2),
                    )
                )
                break

            elif cmd in ("limpar", "clear"):
                bot.clear_history()
                message_count = 0
                console.clear()
                print_banner()
                console.print("[green]✅ Histórico limpo![/green]\n")
                continue

            elif cmd in ("ajuda", "help", "?"):
                console.print(
                    Panel(
                        Markdown(HELP_TEXT),
                        title="[gold1]Ajuda[/gold1]",
                        border_style="dim",
                    )
                )
                continue

            elif cmd == "sessao":
                elapsed = datetime.datetime.now() - session_start
                console.print(
                    Panel(
                        f"⏱️  Duração: [bold]{int(elapsed.total_seconds()/60)}m[/bold]\n"
                        f"💬 Mensagens: [bold]{message_count}[/bold]",
                        title="[gold1]Sessão Atual[/gold1]",
                        border_style="dim",
                        padding=(0, 2),
                    )
                )
                continue

            # ── Envia mensagem ao bot ───────────────────────
            with console.status(
                "[dim]Consultando o FinanceBot Pro...[/dim]", spinner="dots"
            ):
                response = bot.chat(user_input)

            message_count += 1
            console.print(format_response(response))

        except KeyboardInterrupt:
            console.print("\n\n[dim]Encerrando... Até logo! 💰[/dim]")
            break
        except Exception as e:
            console.print(f"[bold red]❌ Erro: {e}[/bold red]")


if __name__ == "__main__":
    main()
