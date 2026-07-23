import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

@dataclass
class Config:
    last_mode: str = "1"
    cookie_save: bool = True
    theme: str = "default"

class Sel:
    """Centralized Selectors for Arena.ai"""
    INPUT = [
        'textarea[placeholder*="message" i]',
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
        'textarea',
    ]
    SEND = [
        'button[aria-label*="send" i]',
        'button[type="submit"]',
        'button:has-text("Send")',
        'button[data-testid*="send"]'
    ]
    STOP = [
        'button[aria-label*="stop" i]',
        'button:has-text("Stop")',
    ]
    ASSISTANT = [
        '[data-testid="assistant-message"]',
        '.assistant-message',
        '[role="article"]:last-child',
        '.message:last-child',
        'div[class*="message"][class*="assistant"]:last-child',
        'div[class*="response"]:last-child',
    ]
    USER_MENU = [
        '[data-testid="user-menu"]',
        '[aria-label*="account" i]',
        '[aria-label*="profile" i]',
        'img[alt*="avatar" i]',
        'button[class*="avatar"]',
    ]
    LOGIN_BTN = [
        'text=Log In',
        'text=Sign In'
    ]

MODES: Dict[str, Tuple[str, str]] = {
    "1": ("Chat",         "https://arena.ai/"),
    "2": ("Code",         "https://arena.ai/code"),
    "3": ("Text / Write", "https://arena.ai/text"),
    "4": ("Search Web",   "https://arena.ai/search"),
    "5": ("Image",        "https://arena.ai/image"),
    "6": ("Direct",       "https://arena.ai/direct"),
    "7": ("Side by Side", "https://arena.ai/side-by-side"),
}

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".arena_cli"
        self.config_file = self.config_dir / "config.json"
        self.cookies_file = self.config_dir / "cookies.json"
        self.history_dir = self.config_dir / "history"
        
        self._ensure_dirs()
        self.config = self._load_config()

    def _ensure_dirs(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> Config:
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return Config(**{k: v for k, v in data.items() if hasattr(Config, k)})
            except Exception:
                pass
        return Config()

    def save_config(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config.__dict__, f, indent=2)

    def has_valid_cookies(self) -> bool:
        return self.cookies_file.exists() and self.cookies_file.stat().st_size > 10

    def load_cookies(self) -> Optional[list]:
        if self.has_valid_cookies():
            try:
                with open(self.cookies_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def save_cookies(self, cookies: list):
        if self.config.cookie_save:
            with open(self.cookies_file, "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=2)

cfg_mgr = ConfigManager()
