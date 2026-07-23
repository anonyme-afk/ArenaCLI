import asyncio
import typer
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings

from core.config import cfg_mgr, MODES
from core.browser import ArenaBrowser
from core.history import HistoryManager
from ui.display import (
    print_banner, print_status, print_models_table, 
    print_user_message, print_bot_message, print_info, print_error, print_success
)
from ui.menus import choose_mode_menu
from utils.logging import setup_logger

app = typer.Typer(help="Arena.ai CLI V2 - Wrapper Playwright Premium")

COMMANDS = ["/help", "/mode", "/models", "/clear", "/save", "/history", "/quit", "/exit", "/q", "/doctor"]

async def chat_loop(browser: ArenaBrowser, history: HistoryManager):
    print_info("[cyan]Vérification de la session...[/cyan]")
    logged_in = await browser.check_logged_in()
    
    if not logged_in:
        print_error("Non connecté. Lance [bold]python arena.py --login[/bold] pour te connecter d'abord.")
        await browser.stop()
        return

    mode_key = cfg_mgr.config.last_mode
    mode_name = MODES.get(mode_key, MODES["1"])[0]
    
    await browser.navigate_to_mode(mode_key)
    print_status(True, mode_name)
    print_success("Prêt ! Tape /help pour les commandes. Utilise Alt+Entrée pour un saut de ligne.\n")

    # Setup prompt toolkit
    completer = WordCompleter(COMMANDS, ignore_case=True)
    kb = KeyBindings()

    @kb.add('escape', 'enter')
    @kb.add('a-enter')
    def _(event):
        """Insert a newline when Alt+Enter is pressed."""
        event.current_buffer.insert_text('\n')

    @kb.add('enter')
    def _(event):
        """Submit when Enter is pressed."""
        event.current_buffer.validate_and_handle()

    session = PromptSession(
        message="❯ ",
        completer=completer,
        key_bindings=kb,
        multiline=True
    )

    while True:
        try:
            # We must run prompt_toolkit asynchronously
            user_input = await session.prompt_async()
        except (KeyboardInterrupt, EOFError):
            print_info("\n[dim]Au revoir ![/dim]")
            break

        text = user_input.strip()
        if not text:
            continue

        cmd = text.lower()
        if cmd in ("/quit", "/exit", "/q"):
            print_info("[dim]Au revoir ![/dim]")
            break
            
        elif cmd == "/help":
            print_info("[bold]/mode[/bold]    → Changer de mode")
            print_info("[bold]/models[/bold]  → Voir les modèles disponibles")
            print_info("[bold]/clear[/bold]   → Nouvelle conversation")
            print_info("[bold]/save[/bold]    → Sauvegarder la conversation (Markdown/JSON)")
            print_info("[bold]/history[/bold] → Voir l'historique récent")
            print_info("[bold]/doctor[/bold]  → Diagnostiquer la session (debug)")
            print_info("[bold]/quit[/bold]    → Quitter")
            
        elif cmd == "/mode":
            mode_key = choose_mode_menu(cfg_mgr.config.last_mode)
            cfg_mgr.config.last_mode = mode_key
            cfg_mgr.save_config()
            
            mode_name = MODES[mode_key][0]
            await browser.navigate_to_mode(mode_key)
            print_success(f"Basculé sur le mode : {mode_name}")
            history.clear_session()
            
        elif cmd == "/models":
            models = await browser.get_available_models()
            print_models_table(models)
            
        elif cmd == "/clear":
            await browser.navigate_to_mode(mode_key)
            history.clear_session()
            print_info("[dim]Conversation réinitialisée.[/dim]")
            
        elif cmd == "/save":
            res = history.save_session()
            print_success(res)
            
        elif cmd == "/history":
            recent = history.get_recent_history()
            if not recent:
                print_info("Aucun historique trouvé.")
            else:
                print_info("[cyan]Fichiers d'historique récents :[/cyan]")
                for f in recent:
                    print_info(f"  • {f.name}")
                    
        elif cmd == "/doctor":
            print_info("[yellow]Lancement du diagnostic...[/yellow]")
            is_logged = await browser.check_logged_in()
            print_info(f"Connecté : {is_logged}")
            if browser.debug:
                from utils.logging import dump_diagnostic_info
                ss, html = await dump_diagnostic_info(browser.page, "doctor")
                print_info(f"Fichiers de diagnostic générés.")
                
        else:
            # Send message
            history.add_message("user", text)
            print_user_message(text)
            
            response = await browser.send_message(text)
            
            history.add_message("assistant", response)
            print_bot_message(response)


@app.command()
def main(
    login: bool = typer.Option(False, "--login", help="Ouvre un navigateur visible pour te connecter manuellement"),
    visible: bool = typer.Option(False, "--visible", help="Lance en mode navigateur visible"),
    debug: bool = typer.Option(False, "--debug", help="Active les logs et screenshots en cas d'erreur")
):
    print_banner()
    
    if debug:
        setup_logger(debug_mode=True)
        print_info("[yellow]Mode Debug activé.[/yellow]")

    browser = ArenaBrowser(headless=not visible, debug=debug)
    history = HistoryManager()

    async def _run():
        if login:
            await browser.login_visible()
            return
            
        await browser.start()
        try:
            await chat_loop(browser, history)
        finally:
            await browser.stop()

    asyncio.run(_run())

if __name__ == "__main__":
    app()
