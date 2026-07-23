from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from ui.theme import ARENA_THEME, BANNER_ASCII

console = Console(theme=ARENA_THEME)

def print_banner(version: str = "2.0.0"):
    console.print(f"[bold cyan]{BANNER_ASCII}[/bold cyan]")
    console.print(f"[dim]Wrapper non-officiel — Playwright v{version}[/dim]\n")

def print_status(session_active: bool, mode_name: str):
    status_text = "[success]✓ Connecté[/success]" if session_active else "[warning]⚠ Déconnecté[/warning]"
    console.print(f"Statut: {status_text} | Mode: [bold]{mode_name}[/bold]\n")

def print_models_table(models: list[str]):
    if not models:
        console.print("[dim]Aucun modèle détecté.[/dim]")
        return
        
    t = Table(title="Modèles disponibles", border_style="dim cyan")
    t.add_column("Modèle", style="bold white")
    for m in models:
        t.add_row(m)
    console.print(t)

def print_user_message(msg: str):
    console.print(Panel(msg, title="[user_msg]Toi[/user_msg]", border_style="yellow", padding=(0, 2)))

def print_bot_message(msg: str):
    md = Markdown(msg)
    console.print(Panel(md, title="[bot_msg]Arena[/bot_msg]", border_style="cyan", padding=(1, 2)))

def print_error(msg: str):
    console.print(f"[error]Erreur:[/error] {msg}")

def print_info(msg: str):
    console.print(f"[info]{msg}[/info]")

def print_success(msg: str):
    console.print(f"[success]{msg}[/success]")

def get_spinner(msg: str):
    return console.status(f"[cyan]{msg}[/cyan]")
