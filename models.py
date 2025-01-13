from datetime import datetime
from typing import Optional, List, Dict

class Task:
    def __init__(self, description: str, due_date: Optional[str], priority: str, category: str):
        # Add input validation
        if not description:
            raise ValueError("Task description required")
        if due_date and not self._validate_date(due_date):
            raise ValueError("Invalid date format")
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.completed = False

    def to_dict(self) -> Dict:
        return {
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "category": self.category,
            "completed": self.completed
        }

class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at
        }
