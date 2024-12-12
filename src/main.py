from database import Database
from assistant import Assistant
import time

DB_FILE = "assistant_data.json"
def main():
      db = Database(DB_FILE)
      assistant = Assistant(db)
    
      assistant.daily_greeting()
      assistant.check_pending_tasks()

      while True:
          print("\nWhat would you like to do? I can help you with:")
          print("1. Add a new task")
          print("2. Show your tasks")
          print("3. Mark a task complete")
          print("4. Write a note")
          print("5. Read your notes")
          print("6. Check your progress")
          print("7. Say goodbye")
          print("8. Read a webpage")
          print("9. Read a document")
          print("10. Search saved documents")

          choice = input("\nJust type a number or tell me what you need: ").strip()
        
          if choice == "1":
              print("Let's add a new task!")
              description = input("What's the task about? ")
              due_date = input("When does it need to be done? (YYYY-MM-DD or press Enter to skip) ")
              priority = input("How important is it? (High/Medium/Low) ").capitalize()
              category = input("What category should I file this under? (Work/Personal/etc) ")
            
              assistant.add_task(description, due_date or None, priority or "Medium", category or "General")
              print("Got it! I've added your task to the list.")
            
              time.sleep(1)
              print("Anything else you'd like to add?")
            
          elif choice == "7":
              print(f"Goodbye {assistant.user_name}! Have a great day!")
              break
        
          elif choice == "8":
              url = input("What's the webpage URL you'd like me to read? ")
              try:
                  content = document_reader.read_webpage(url)
                  assistant.save_document_content(content)
                  print(f"I've read and saved the content from {content['title']}")
                  print("Would you like me to show you a summary? (yes/no)")
                  if input().lower().startswith('y'):
                      print(f"\nTitle: {content['title']}")
                      print(f"First 200 characters: {content['content'][:200]}...")
              except Exception as e:
                  print(f"I had trouble reading that webpage. Make sure the URL is correct.")
        
          elif choice == "9":
              filepath = input("What's the path to your document? ")
              try:
                  content = document_reader.read_file(filepath)
                  assistant.save_document_content(content)
                  print(f"I've successfully read {content['title']}")
                  print("\nWould you like to:")
                  print("1. See a preview")
                  print("2. Save and continue")
                  preview_choice = input("Enter your choice (1/2): ")
                  
                  if preview_choice == "1":
                      preview_length = 500
                      print(f"\nPreview of {content['title']}:")
                      print("-" * 50)
                      print(content['content'][:preview_length] + "...")
                      print("-" * 50)
              except Exception as e:
                  print(f"I encountered an issue: {str(e)}")
        
          elif choice == "10":
              query = input("What would you like to search for in your documents? ")
              results = assistant.search_documents(query)
              if results:
                  print(f"\nI found {len(results)} matching documents:")
                  for i, doc in enumerate(results, 1):
                      print(f"\n{i}. {doc['title']} ({doc['type']})")
                      print(f"Source: {doc['source']}")
                    
                  doc_choice = input("\nEnter a number to see the full content (or press Enter to skip): ")
                  if doc_choice.isdigit() and 0 < int(doc_choice) <= len(results):
                      selected = results[int(doc_choice) - 1]
                      print(f"\n--- {selected['title']} ---")
                      print(selected['content'])
              else:
                  print("I couldn't find any documents matching your search.")
if __name__ == "__main__":
    main()