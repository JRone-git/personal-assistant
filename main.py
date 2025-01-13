from database import Database
from assistant import Assistant
from cli import main_loop

DB_FILE = "assistant_data.json"

def main():
    db = Database(DB_FILE)
    assistant = Assistant(db)
    
    assistant.daily_greeting()
    assistant.check_pending_tasks()

    main_loop(assistant)

if __name__ == "__main__":
    main()
