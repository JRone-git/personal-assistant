# Personal Assistant

A versatile personal assistant application designed to help you manage your tasks, notes, and documents efficiently. This project combines a command-line interface (CLI) with a user-friendly web interface, providing flexibility and ease of use.

This project now includes a web interface with chat functionality for easier interaction.

## Project Overview

This personal assistant application is built using Python and Flask, and it provides the following core functionalities:

*   **Task Management:** Add, view, edit, and complete tasks with due dates and priorities.
*   **Note Taking:** Create, save, and retrieve notes with titles and content.
*   **Document Management:** Upload, store, and view documents, including PDFs, images, and text files.
*   **Smart Document Processing:** Automatically summarize, extract keywords, and categorize documents.
*   **Web Interface:** A user-friendly web interface for interacting with the assistant, including a chat feature.
*   **Command-Line Interface (CLI):** A command-line interface for managing tasks, notes, and documents.

## Features

*   **Task Management:**
    *   Add tasks with descriptions, due dates, and priorities.
    *   View a list of all tasks, sorted by due date.
    *   Mark tasks as complete.
    *   Edit existing tasks.
*   **Note Taking:**
    *   Create notes with titles and content.
    *   View a list of all notes, sorted by creation date.
*   **Document Management:**
    *   Upload documents of various types (PDF, images, text files).
    *   View a list of all documents.
    *   View the content of individual documents.
    *   Automatic summarization, keyword extraction, and categorization of documents.
*   **Web Interface:**
    *   User-friendly web interface for managing tasks, notes, and documents.
    *   Chat functionality for interacting with the assistant.
*   **Command-Line Interface (CLI):**
    *   Command-line interface for managing tasks, notes, and documents.

## Technologies Used

*   **Python:** The core programming language.
*   **Flask:** A micro web framework for building the web interface.
*   **Flask-SQLAlchemy:** An extension for interacting with databases.
*   **Flask-Migrate:** An extension for managing database migrations.
*   **Transformers:** A library for natural language processing tasks (summarization).
*   **Pillow:** A library for image processing.
*   **Pytesseract:** A library for optical character recognition (OCR).
*   **PyPDF2:** A library for working with PDF files.
*   **Newspaper3k:** A library for extracting and curating articles from the web.
*   **KeyBERT:** A library for keyword extraction.
*   **SQLite:** A lightweight database for storing data.

## Running the Web Interface

To get the web interface up and running, follow these steps:

1.  **Navigate to the Project Directory:**

    Open your terminal or command prompt and navigate to the `assistantweb` directory within your project:

    ```bash
    cd assistantweb
    ```

2.  **Set Up the Virtual Environment:**

    It's highly recommended to use a virtual environment to manage project dependencies. If you haven't already, create and activate one:

    *   **Windows:**

        ```bash
        .\venv312\Scripts\activate
        ```

    *   **macOS/Linux:**

        ```bash
        source venv312/bin/activate
        ```

3.  **Install Dependencies:**

    Install all the required Python packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Start the Flask Development Server:**

    Run the Flask application to start the web server:

    ```bash
    flask run
    ```

    You'll see output in your terminal indicating the server is running, along with the address where it's accessible.

5.  **Access the Web Interface:**

    Open your web browser and go to the address provided in the terminal output (usually `http://127.0.0.1:5000`). You should now see the web interface.

## Running the CLI

To run the command-line interface, follow these steps:

1.  **Navigate to the Project Directory:**

    Open your terminal or command prompt and navigate to the root directory of the project:

    ```bash
    cd <project_root_directory>
    ```

2.  **Activate the virtual environment:**

    ```bash
    .\venv312\Scripts\activate
    ```
    (or `source venv312/bin/activate` on macOS/Linux)

3.  **Run the CLI:**

    ```bash
    python cli.py
    ```

    This will start the command-line interface.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes.
4.  Submit a pull request.

## License

This project is licensed under the MIT License.

