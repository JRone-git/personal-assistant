import json
import os
from typing import Dict, List

class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.data = self._load_or_initialize()

    def _load_or_initialize(self) -> Dict:
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return {"tasks": [], "notes": []}

    def save(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=4)

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