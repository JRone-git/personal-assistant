import json
import os
import logging
from typing import Dict, Optional
from contextlib import contextmanager

class Database:
    def __init__(self, db_file: str):
        # Add proper validation and initialization
        if not db_file.endswith('.json'):
            raise ValueError("Database file must be JSON")
        self.db_file = db_file
        self.setup_logging()
        self._validate_db_file()
        self.data = self._load_or_initialize()

    def _load_or_initialize(self) -> Dict:
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return {"tasks": [], "notes": []}

    @contextmanager
    def atomic_write(self):
        """Atomic file writing with backup"""
        backup_file = f"{self.db_file}.bak"
        try:
            if os.path.exists(self.db_file):
                os.replace(self.db_file, backup_file)
            yield
            if os.path.exists(backup_file):
                os.remove(backup_file)
        except Exception as e:
            if os.path.exists(backup_file):
                os.replace(backup_file, self.db_file)
            raise e

    def save(self):
        # Add proper atomic file operations
        temp_file = f"{self.db_file}.tmp"
        try:
            with open(temp_file, 'w') as f:
                json.dump(self.data, f, indent=4)
            os.replace(temp_file, self.db_file)
        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise

    def add_task(self, task_dict: Dict):
        self.data["tasks"].append(task_dict)
        self.save()

    def add_note(self, note_dict: Dict):
        self.data["notes"].append(note_dict)
        self.save()

    def save_document(self, document_data):
        if "documents" not in self.data:
            self.data["documents"] = []
        self.data["documents"].append(document_data)
        self.save()