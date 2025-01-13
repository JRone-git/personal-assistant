from typing import Dict, Optional
from datetime import datetime

class BaseTask:
    def __init__(self, description: str, due_date: Optional[str] = None):
        self.description = description
        self.due_date = due_date
        self.completed = False

    def to_dict(self) -> Dict:
        return {
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed
        }
