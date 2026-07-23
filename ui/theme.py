from rich.theme import Theme

# ASCII Banner
BANNER_ASCII = """
    _                      ____ _     ___ 
   / \   _ __ ___ _ __   / ___| |   |_ _|
  / _ \ | '__/ _ \ '_ \ | |   | |    | | 
 / ___ \| | |  __/ | | || |___| |___ | | 
/_/   \_\_|  \___|_| |_(_)____|_____|___|
"""

ARENA_THEME = Theme({
    "info": "dim cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "user_msg": "bold yellow",
    "bot_msg": "bold cyan",
})
