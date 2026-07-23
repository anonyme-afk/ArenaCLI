import json
from pathlib import Path
from datetime import datetime
from core.config import cfg_mgr
from typing import List, Dict

class HistoryManager:
    def __init__(self):
        self.history_dir = cfg_mgr.history_dir
        self.current_session: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        """Add a message to the current session."""
        self.current_session.append({"role": role, "content": content})

    def save_session(self) -> str:
        """Save the current session to JSON and Markdown formats."""
        if not self.current_session:
            return "Aucun message à sauvegarder."

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        title = self.current_session[0]["content"][:30].replace(" ", "_").replace("/", "_")
        if not title:
            title = "session"
        
        base_filename = f"{timestamp}_{title}"
        json_path = self.history_dir / f"{base_filename}.json"
        md_path = self.history_dir / f"{base_filename}.md"

        # Save JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.current_session, f, indent=2, ensure_ascii=False)

        # Save Markdown
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Arena Session - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for msg in self.current_session:
                role = "👤 **User**" if msg["role"] == "user" else "🤖 **Arena**"
                f.write(f"### {role}\n\n")
                f.write(f"{msg['content']}\n\n")
                f.write("---\n\n")

        return f"Session sauvegardée dans {self.history_dir}"

    def get_recent_history(self, limit: int = 10) -> List[Path]:
        """Get a list of recent markdown history files."""
        md_files = list(self.history_dir.glob("*.md"))
        md_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return md_files[:limit]

    def clear_session(self):
        """Clear the current session."""
        self.current_session = []
