from assistant import Assistant
import time

def display_menu():
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
    print("11. Edit a task")

def get_user_choice():
    return input("\nJust type a number or tell me what you need: ").strip()

def handle_add_task(assistant):
    print("Let's add a new task!")
    description = input("What's the task about? ")
    due_date = input("When does it need to be done? (YYYY-MM-DD or press Enter to skip) ")
    priority = input("How important is it? (High/Medium/Low) ").capitalize()
    category = input("What category should I file this under? (Work/Personal/etc) ")

    assistant.add_task(description, due_date or None, priority or "Medium", category or "General")
    print("Got it! I've added your task to the list.")
    time.sleep(1)
    print("Anything else you'd like to add?")

def handle_show_tasks(assistant):
    tasks = assistant.get_tasks()
    if tasks:
        print("\nYour tasks:")
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task['description']} (Due: {task.get('due_date', 'N/A')}, Priority: {task.get('priority', 'N/A')}, Category: {task.get('category', 'N/A')})")
    else:
        print("\nYou have no tasks.")

def handle_mark_task_complete(assistant):
    tasks = assistant.get_tasks()
    if tasks:
        print("\nWhich task would you like to mark as complete?")
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task['description']}")
        
        try:
            choice = int(input("\nEnter the task number: "))
            if assistant.mark_task_complete(choice):
                print("Task marked as complete.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("\nYou have no tasks to mark as complete.")

def handle_write_note(assistant):
    pass # Implement this later

def handle_read_notes(assistant):
    pass # Implement this later

def handle_check_progress(assistant):
    pass # Implement this later

def handle_say_goodbye(assistant):
    print(f"Goodbye {assistant.user_name}! Have a great day!")
    return True

def handle_read_webpage(assistant):
    url = input("What's the webpage URL you'd like me to read? ")
    try:
        content = assistant.document_reader.read_webpage(url)
        assistant.save_document_content(content)
        print(f"I've read and saved the content from {content['title']}")
        print("Would you like me to show you a summary? (yes/no)")
        if input().lower().startswith('y'):
            print(f"\nTitle: {content['title']}")
            print(f"First 200 characters: {content['content'][:200]}...")
    except Exception as e:
        print(f"I had trouble reading that webpage. Make sure the URL is correct.")

def handle_read_document(assistant):
    filepath = input("What's the path to your document? ")
    encrypt = input("Encrypt this file? (yes/no): ").lower().startswith('y')
    password = None
    if encrypt:
        password = input("Enter a password for encryption: ")
    try:
        if encrypt and password:
            with open(filepath, 'rb') as file:
                file_data = file.read()
            encrypted_data = assistant.document_reader.encrypt_file(filepath, password)
            encrypted_filepath = filepath + ".enc"
            with open(encrypted_filepath, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)
            content = assistant.document_reader.read_file(encrypted_filepath, password, encrypted=True)
            os.remove(encrypted_filepath)
        else:
            content = assistant.document_reader.read_file(filepath)
        assistant.save_document_content(content)
        print(f"I've successfully read {content['title']}")
        print("\nWould you like to:")
        print("1. See a preview")
        print("2. See a summary")
        print("3. Save and continue")
        preview_choice = input("Enter your choice (1/2/3): ")
        
        if preview_choice == "1":
            preview_length = 500
            print(f"\nPreview of {content['title']}:")
            print("-" * 50)
            print(content['content'][:preview_length] + "...")
            print("-" * 50)
        elif preview_choice == "2":
            print(f"\nSummary of {content['title']}:")
            print("-" * 50)
            print(content['summary'])
            print("-" * 50)
    except Exception as e:
        print(f"I encountered an issue: {str(e)}")

def handle_search_documents(assistant):
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

def handle_edit_task(assistant):
    tasks = assistant.get_tasks()
    if tasks:
        print("\nWhich task would you like to edit?")
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task['description']}")
        
        try:
            choice = int(input("\nEnter the task number: "))
            if 0 < choice <= len(tasks):
                task_index = choice - 1
                print("\nWhat would you like to edit?")
                description = input(f"New description (leave blank to keep '{tasks[task_index]['description']}'): ")
                due_date = input(f"New due date (YYYY-MM-DD, leave blank to keep '{tasks[task_index].get('due_date', 'N/A')}'): ")
                priority = input(f"New priority (High/Medium/Low, leave blank to keep '{tasks[task_index].get('priority', 'N/A')}'): ").capitalize()
                category = input(f"New category (leave blank to keep '{tasks[task_index].get('category', 'N/A')}'): ")
                
                if assistant.edit_task(task_index, description or None, due_date or None, priority or None, category or None):
                    print("Task updated successfully.")
                else:
                    print("Failed to update task.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("\nYou have no tasks to edit.")

def main_loop(assistant):
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            handle_add_task(assistant)
        elif choice == "2":
            handle_show_tasks(assistant)
        elif choice == "3":
            handle_mark_task_complete(assistant)
        elif choice == "4":
            handle_write_note(assistant)
        elif choice == "5":
            handle_read_notes(assistant)
        elif choice == "6":
            handle_check_progress(assistant)
        elif choice == "7":
            if handle_say_goodbye(assistant):
                break
        elif choice == "8":
            handle_read_webpage(assistant)
        elif choice == "9":
            handle_read_document(assistant)
        elif choice == "10":
            handle_search_documents(assistant)
        elif choice == "11":
            handle_edit_task(assistant)
        else:
            print("Invalid choice. Please try again.")