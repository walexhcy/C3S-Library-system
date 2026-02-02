import json
import os
from typing import Any, Dict


class JsonStorage:
    """Reads/writes the app state as JSON."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self) -> None:
        folder = os.path.dirname(self.filepath)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.filepath):
            self.save({
                "books": [],
                "members": [],
                "loans": []
            })

    def load(self) -> Dict[str, Any]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data: Dict[str, Any]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
