import questionary
from core.config import MODES

def choose_mode_menu(default_key: str = "1") -> str:
    """Affiche un menu interactif avec questionary pour choisir le mode."""
    choices = [
        questionary.Choice(
            title=f"{key} - {name} ({url})",
            value=key
        )
        for key, (name, url) in MODES.items()
    ]
    
    # Trouver le choix par défaut
    default_choice = next((c for c in choices if c.value == default_key), choices[0])
    
    answer = questionary.select(
        "Choisis un mode :",
        choices=choices,
        default=default_choice,
        style=questionary.Style([
            ('qmark', 'fg:#00ffff bold'),
            ('question', 'bold'),
            ('answer', 'fg:#00ffff bold'),
            ('pointer', 'fg:#00ffff bold'),
            ('highlighted', 'fg:#00ffff bold'),
            ('selected', 'fg:#00ffff'),
            ('separator', 'fg:#cc5454'),
            ('instruction', ''),
            ('text', ''),
            ('disabled', 'fg:#858585 italic')
        ])
    ).ask()
    
    return answer if answer else default_key
