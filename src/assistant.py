from typing import List, Dict
from datetime import datetime
from models import Task, Note
from database import Database
class Assistant:
    def __init__(self, db: Database):
        self.db = db
        self.user_name = self._get_or_ask_name()

    def _get_or_ask_name(self) -> str:
        if "user_name" in self.db.data:
            return self.db.data["user_name"]
        name = input("Hi! I'm your personal assistant. What's your name? ")
        self.db.data["user_name"] = name
        self.db.save()
        return name

    def check_pending_tasks(self):
        pending_tasks = self.get_tasks(filter_completed=True)
        if pending_tasks:
            print(f"\nHey {self.user_name}, I noticed you have some pending tasks:")
            for i, task in enumerate(pending_tasks):
                print(f"{i + 1}. {task['description']}")
                response = input("Did you complete this task? (yes/no): ").lower()
                if response.startswith('y'):
                    self.complete_task(i)
                    print("Great job! I've marked that as completed.")
                else:
                    importance = input("Would you like to work on it now? (yes/no): ").lower()
                    if importance.startswith('y'):
                        print("That's the spirit! Let me know when you're done.")
                    else:
                        new_date = input("When would you like to do it? (YYYY-MM-DD): ")
                        if new_date:
                            task['due_date'] = new_date
                            self.db.save()
                            print(f"I've updated the due date to {new_date}")

    def daily_greeting(self):
        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
            
        print(f"\n{greeting}, {self.user_name}!")
        
        if self.get_tasks(filter_completed=True):
            print("You have some tasks waiting for your attention.")
        else:
            print("You're all caught up with your tasks!")

    def add_task(self, description: str, due_date: str, priority: str, category: str):
        task = Task(description, due_date, priority, category)
        self.db.add_task(task.to_dict())

    def get_tasks(self, filter_completed: bool = False) -> List[dict]:
        return [task for task in self.db.data["tasks"] 
                if not filter_completed or not task["completed"]]

    def complete_task(self, index: int):
        if 0 <= index < len(self.db.data["tasks"]):
            self.db.data["tasks"][index]["completed"] = True
            self.db.save()
            return True
        return False

    def add_note(self, title: str, content: str):
        note = Note(title, content)
        self.db.add_note(note.to_dict())

    def get_notes(self, search_term: str = "") -> List[dict]:
        return [note for note in self.db.data["notes"] 
                if search_term.lower() in note["title"].lower() 
                or search_term.lower() in note["content"].lower()]

# Add to existing Assistant class:

def save_document_content(self, document_data: Dict[str, str]):
    if "documents" not in self.db.data:
        self.db.data["documents"] = []
    
    self.db.data["documents"].append({
        "title": document_data["title"],
        "content": document_data["content"],
        "source": document_data["source"],
        "type": document_data["type"],
        "date_added": datetime.now().isoformat()
    })
    self.db.save()

def search_documents(self, query: str) -> List[Dict]:
    if "documents" not in self.db.data:
        return []
    
    return [doc for doc in self.db.data["documents"] 
            if query.lower() in doc["content"].lower() 
            or query.lower() in doc["title"].lower()]
