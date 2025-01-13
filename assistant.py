from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta
from models import Task, Note
from database import Database
from document_reader import DocumentReader
from ratelimit import limits, sleep_and_retry, RateLimiter

class Assistant:
    def __init__(self, db: Database):
        self.setup_logging()
        self._validate_db(db)
        self.db = db
        self.document_reader = DocumentReader()
        self.user_name = self._get_or_ask_name()
        self.tasks = self.db.data.get("tasks", [])
        self.notes = self.db.data.get("notes", [])
        self.documents = self.db.data.get("documents", [])

        # Add proper validation
        if not isinstance(db, Database):
            raise TypeError("Invalid database instance")
            
        # Add rate limiting for critical operations
        self.rate_limiter = RateLimiter(max_calls=10, period=60)

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='assistant.log'
        )

    def _get_or_ask_name(self) -> str:
        if "user_name" in self.db.data:
            return self.db.data["user_name"]
        name = input("Hi! I'm your personal assistant. What's your name? ")
        self.db.data["user_name"] = name
        self.db.save()
        return name

    @sleep_and_retry
    @limits(calls=10, period=60)
    def encrypt_file(self, filepath: str, password: str) -> bytes:
        """Rate-limited encryption to prevent brute force attempts"""
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        return self.document_reader.encrypt_file(filepath, password)

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
                            task_index = self.tasks.index(task)
                            self.tasks[task_index]['due_date'] = new_date
                            self.db.data["tasks"][task_index]['due_date'] = new_date
                            self.db.save()
                            print(f"I've updated the due date to {new_date}")
            self.tasks = self.db.data.get("tasks", [])

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

    def add_task(self, description: str, due_date: Optional[str], priority: str, category: str) -> bool:
        """Add a new task with validation"""
        if not description:
            raise ValueError("Task description cannot be empty")
            
        if due_date and not self._validate_date(due_date):
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        task = Task(description, due_date, priority, category)
        return self.db.add_task(task.to_dict())

    def get_tasks(self, filter_completed: bool = False) -> List[dict]:
        return [task for task in self.tasks 
                if not filter_completed or not task["completed"]]

    def complete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = True
            self.db.data["tasks"][index]["completed"] = True
            self.db.save()
            return True
        return False
    
    def mark_task_complete(self, index: int):
        if 0 <= index - 1 < len(self.tasks):
            return self.complete_task(index - 1)
        return False
    
    def edit_task(self, index: int, description: str = None, due_date: str = None, priority: str = None, category: str = None):
        if 0 <= index < len(self.tasks):
            if description:
                self.tasks[index]["description"] = description
                self.db.data["tasks"][index]["description"] = description
            if due_date:
                self.tasks[index]["due_date"] = due_date
                self.db.data["tasks"][index]["due_date"] = due_date
            if priority:
                self.tasks[index]["priority"] = priority
                self.db.data["tasks"][index]["priority"] = priority
            if category:
                self.tasks[index]["category"] = category
                self.db.data["tasks"][index]["category"] = category
            self.db.save()
            return True
        return False

    def add_note(self, title: str, content: str):
        note = Note(title, content)
        self.db.add_note(note.to_dict())
        self.notes.append(note.to_dict())

    def get_notes(self, search_term: str = "") -> List[dict]:
        return [note for note in self.notes
                if search_term.lower() in note["title"].lower() 
                or search_term.lower() in note["content"].lower()]

    def save_document_content(self, content):
        document_data = {
            "title": content["title"],
            "content": content["content"],
            "source": content["source"],
            "type": content["type"],
            "date_added": str(datetime.now()),
            "summary": content["summary"]
        }
        self.db.save_document(document_data)
        self.documents.append(document_data)

    def search_documents(self, query: str) -> List[Dict]:
        return [doc for doc in self.documents
                if query.lower() in doc["content"].lower() 
                or query.lower() in doc["title"].lower()]